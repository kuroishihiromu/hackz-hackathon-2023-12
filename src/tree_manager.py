#自作のdatabaseモジュールをインポート
from database.models import *
import networkx as nx
from collections import deque

class TreeManager:
  def __init__(self,Cluster):
    self.cluster = Cluster
    self.tree = nx.DiGraph()
    self.root_user = None

  def create_tree(self):
    
    # clusterに所属するユユーザーを取得
    users = self.cluster.users
    
    # userの過去１０日間のsleep_levelの平均値を用いて降順にソート
    sorted_users = sorted(users, reverse=True, key=lambda x: sum([setting.yesterday_sleep_level for setting in x.settings])/len(x.settings))
    
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

    return self.tree
