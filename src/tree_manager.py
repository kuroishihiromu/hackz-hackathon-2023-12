#自作のdatabaseモジュールをインポート
from database.models import *
import networkx as nx
from collections import deque
from datetime import datetime, timedelta
import time
import pickle
import random
import threading
from database.threading_db_conector import DBConnector


class TreeManager:
    def __init__(self,Cluster):
        self.cluster = Cluster
        self.tree = nx.DiGraph()
        self.root_user_id = None
        self.process_id = random.randint(10000000, 99999999)
        self.tree_index = None
    
    def create_tree(self,tree_index):
        
        self.tree_index = tree_index
        # clusterに所属するユーザーを取得
        users = self.cluster.users
        
        # 現在の日付から10日前の日付を計算
        ten_days_ago = datetime.now() - timedelta(days=10)
        
        # 過去10日間の設定のみを考慮して平均値を計算し、その平均値でユーザーを降順にソート
        sorted_users = sorted(users, reverse=True, key=lambda x: 
            sum(setting.yesterday_sleep_level for setting in x.settings if setting.setting_at >= ten_days_ago)
            / len([setting for setting in x.settings if setting.setting_at >= ten_days_ago]))

        
        # 一番sleep_levelが高いユーザーをroot_userとする
        self.root_user_id = sorted_users[0].id
        
        # 空のdeque（キュー）を作成
        queue = deque()
        
        # キューに要素を追加
        for user in sorted_users:
            queue.append(user)
        
        ################
        ### 木の構築 ###
        ################

        # キューからユーザーを取り出し、木に追加
        count = 0
        while queue:
            user = queue.popleft()
            self.tree.add_node(user.id)

            if count == 0:
                self.root_user = user
            elif count <= 2:
                self.tree.add_edge(sorted_users[count - 1].id, user.id)
            elif count <= 6:
                self.tree.add_edge(sorted_users[2].id, user.id)
            elif count <= 8:
                self.tree.add_edge(sorted_users[3].id, user.id)
            elif count <= 10:
                self.tree.add_edge(sorted_users[4].id, user.id)
            elif count <= 12:
                self.tree.add_edge(sorted_users[5].id, user.id)
            elif count <= 14:
                self.tree.add_edge(sorted_users[6].id, user.id)

            count += 1
        
        # プロセスの登録
        db.session.add(Process(process_id=self.process_id, tree_index=self.tree_index, status='waiting'))
        db.session.commit()

        return True
    
    def start_threading_process(self,user_id):
        thread = threading.Thread(target=self.wake_up_child,args=(user_id,))
        thread.start()
        connector = DBConnector('mysql://user:password@db:3306/mydatabase')
        connector.setup()
        connector.start_process(self.process_id)
        return self.process_id
    
    def wake_up_child(self,user_id):
        try:
            ####################################
            # ここでuserのアラームを鳴らす処理 #
            #################################### 
            connector = DBConnector('mysql://user:password@db:3306/mydatabase')
            connector.setup()
            
            
            
            # userが起きたら次の処理へ
            while True:
                
                # 終了フラグを確認
                if connector.check_process_termination_flag(self.process_id):
                    connector.end_process(self.process_id)
                    return True
                
                # userのstatusを更新
                updated_user = connector.get_user(user_id)
                if updated_user.status == True:
                    break
                
                # 5秒待機
                time.sleep(5)
            
            #ルートユーザーの場合、木の深さを1に設定 
            if user_id == self.root_user_id:
                connector.update_depth(self.process_id, 1)
            else:
                # user_idのノードの深さを計算
                user_depth = nx.shortest_path_length(self.tree, self.root_user_id, user_id)
                # 自分と同じ深さにあるノードのリストを取得
                nodes_at_same_depth = [node for node in self.tree.nodes if nx.shortest_path_length(self.tree, self.root_user_id, node) == user_depth]
                
                if connector.check_users_status(nodes_at_same_depth):
                    # 全員が起きている場合、自分の深さを1つ増やす
                    depth_level = connector.get_process_depth(self.process_id)
                    connector.update_depth(self.process_id, depth_level + 1)
            
            # treeで自身を親に持つuserのidのリストを取得
            child_id_list = list(self.tree.successors(updated_user.id))
            
            # 起きたuserの子供がいなければ終了(枝ごとの終了条件)
            if len(child_id_list) == 0:
                return True
            
            # 全員が起きたら終了（木全体の終了条件）
            if self.check_all_user_awake(connector):
                connector.complete_process(self.process_id)
                return True
            
            
            #再帰
            for child_id in child_id_list:
                self.wake_up_child(child_id)
                
        # 例外処理（プロセスの強制終了）
        except Exception as e:
            connector = DBConnector('mysql://user:password@db:3306/mydatabase')
            connector.setup()
            connector.end_process(self.process_id)
            return False    

    def check_all_user_awake(self,connector):
        # treeの全てのノードを取得
        nodes = list(self.tree.nodes)

        for node in nodes:
            user = connector.get_user(node.id)
            if not user or not user.status:
                # ユーザーが存在しない、またはユーザーのステータスが非活動の場合
                return False

        # すべてのユーザーが起きている（活動している）場合
        return True

    def check_all_user_awake(self,connector):
            # treeの全てのノードを取得
            node_id_list = list(self.tree.nodes)
            for node_id in node_id_list:
                user = connector.get_user(node_id)
                
                if not user or not user.status:
                    # ユーザーが存在しない、またはユーザーのステータスが非活動の場合
                    return False

            # すべてのユーザーが起きている（活動している）場合
            return True

    def check_process_completion_condition(self,connector):
        # 全員が起きている or 定期デーモンによって終了フラグが立てられていたら終了（木全体の終了条件）
        if self.check_all_user_awake(connector):
            connector.complete_process(self.process_id)
            return True
        elif connector.check_process_termination_flag(self.process_id):
            connector.end_process(self.process_id)
            return True
        
        else:
            return False
