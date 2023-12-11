from flask import Flask
from datetime import time , datetime, timedelta
from tree_manager import TreeManager

#自作のdatabaseモジュールをインポート
from database.models import *

class ClusterManager:
    def __init__(self, app):
        self.app = app
        self.clusters = []
        self.trees = []

    def init_cluster(self):

        # 現在の日時を取得
        now = datetime.now()
        # 10日前の日時を計算
        ten_days_ago = now - timedelta(days=10)

        # user_idがキーでtomorrow_wake_up_timeがvalue辞書型を作成
        user_wake_up_time = {}

        #全てのユーザーに対して
        users = User.query.all()
        for user in users:

            # 最新のsetting.tomorrow_wake_up_timeを取得          
            setting = Settings.query.filter(Settings.user_id == user.id).order_by(Settings.setting_at.desc()).first()

            # 無ければデフォルト値として7:00を設定
            if setting is None:
                setting = Settings(
                    user_id = user.id,
                    tomorrow_wake_up_time = time(7, 0),
                    yesterday_sleep_level = 3,
                )
                db.session.add(setting)
                db.session.commit()

            # user_wake_up_timeに追加
            user_wake_up_time[user.id] = setting.tomorrow_wake_up_time
            
        sorted_users = sorted(users,key=lambda x:
            sorted(x.settings, reverse=True, key=lambda y:y.setting_at)[0].tomorrow_wake_up_time)

        # 15人ごとにusersを分割し、分割され集団ごとにclustersを作成し、関係性を定義したのち、clusterをself.clustersに追加
        for i in range(0,len(sorted_users),15):
            users = sorted_users[i:i+15]
            if len(users) < 15:
                set_time = sorted(users[0].settings, reverse=True, key=lambda y:y.setting_at)[0].tomorrow_wake_up_time
            else:
                set_time = sorted(users[7].settings, reverse=True, key=lambda y:y.setting_at)[0].tomorrow_wake_up_time
            cluster = Cluster(middle_wake_up_time = set_time)
            db.session.add(cluster)
            for user in users:
                cluster.users.append(user)
            self.clusters.append(cluster)
            
            tree_manager = TreeManager(cluster)
            self.trees.append(tree_manager.create_tree())
        
        db.session.commit()

    # 一番目のクラスタのユーザー名と起床時刻をテキスト形式で返す
    def get_cluster_info(self):
        cluster = self.clusters[0]
        users = cluster.users
        text = ''
        for user in users:
            text += user.name + ' ' + sorted(user.settings, reverse=True, key=lambda y:y.setting_at)[0].tomorrow_wake_up_time.strftime('%H:%M') + '\n'
        return text
    
    # 実機ユーザーの所属するクラスタを返す。
    def get_device_user_cluster(self):
        
        # 実機ユーザーのidを取得
        user = User.query.filter_by(is_bot=False).first() 
        
        # ユーザーがいなければエラーをスロー
        if user is None:
            raise Exception('実機ユーザーが存在しません。')
        
        # cluster = user.clusters[0]
        cluster = sorted(user.clusters, reverse=True, key=lambda x:x.create_at)[0]
        
        return cluster
