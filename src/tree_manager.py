#自作のdatabaseモジュールをインポート
from database.models import *
import networkx as nx
from collections import deque
from datetime import datetime, timedelta
import pickle
import random
import threading
from database.threading_db_conector import DBConnector


class TreeManager:
    def __init__(self,Cluster):
        self.cluster = Cluster
        self.tree = nx.DiGraph()
        self.root_user = None
        self.process_id = random.randint(10000000, 99999999)
    
    def create_tree(self):
        
        # clusterに所属するユーザーを取得
        users = self.cluster.users
        
        # 現在の日付から10日前の日付を計算
        ten_days_ago = datetime.now() - timedelta(days=10)
        
        # 過去10日間の設定のみを考慮して平均値を計算し、その平均値でユーザーを降順にソート
        sorted_users = sorted(users, reverse=True, key=lambda x: 
            sum(setting.yesterday_sleep_level for setting in x.settings if setting.setting_at >= ten_days_ago)
            / len([setting for setting in x.settings if setting.setting_at >= ten_days_ago]))

        
        # 一番sleep_levelが高いユーザーをroot_userとする
        self.root_user = sorted_users[0]
        
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
            self.tree.add_node(user)

            if count == 0:
                self.root_user = user
            elif count <= 2:
                self.tree.add_edge(sorted_users[count - 1], user)
            elif count <= 6:
                self.tree.add_edge(sorted_users[2], user)
            elif count <= 8:
                self.tree.add_edge(sorted_users[3], user)
            elif count <= 10:
                self.tree.add_edge(sorted_users[4], user)
            elif count <= 12:
                self.tree.add_edge(sorted_users[5], user)
            elif count <= 14:
                self.tree.add_edge(sorted_users[6], user)

            count += 1

        return True

    def wake_up_child(self,user):
        
        ####################################
        # ここでuserのアラームを鳴らす処理 #
        #################################### 
        connector = DBConnector('mysql://user:password@db:3306/mydatabase')
        connector.setup()
        # userが起きたら次の処理へ
        while True:
            # userのstatusを更新
            updated_user = User.query.filter(User.id == user.id).first()
            
            if updated_user.status == True:
                break
            
            # 5秒待機
            time.sleep(5)
        
        # treeで自身を親に持つusersを取得
        children = list(self.tree.successors(user))
        
        # 起きたuserの子供がいなければ終了(枝ごとの終了条件)
        if len(children) == 0:
            return True
        
        # 全員が起きたら終了（木全体の終了条件）
        if self.check_all_user_awake():
            # プロセスを終了（DBの処理を記述）
            return True

        #再帰
        for child in children:
            self.wake_up_child(child)

    def check_all_user_awake(self):
        # treeの全てのノードを取得
        nodes = list(self.tree.nodes)

        for node in nodes:
            user = User.query.filter(User.id == node.id).first()
            if not user or not user.status:
                # ユーザーが存在しない、またはユーザーのステータスが非活動の場合
                return False

        # すべてのユーザーが起きている（活動している）場合
        return True

