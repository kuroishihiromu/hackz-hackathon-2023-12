# モデルのインポート
from datetime import time
from .models import *
from faker import Faker
import random

def database_seeder(app):
    with app.app_context():
        
        faker = Faker('ja_JP')
        users = []
        clusters = []
        settings = []
        
        for _ in range(100):
            
            # 一人のユーザーを作成
            user = User(
                device_id = faker.random_number(digits=12),
                name = faker.name(),
                email = faker.unique.email(),
                password = "password"
            )
            users.append(user)
            
            # 一人のユーザーに対して設定を作成
            
        db.session.add_all(users)
        db.session.commit()



































# # settingsモデルにテストデータを挿入
#         setting = Settings(user_id=user.id, tomorrow_wake_up_time=time(7, 0), yesterday_sleep_level=5)
#         db.session.add(setting)
#         db.session.commit()
        
        
#         # clustersモデルにテストデータを挿入
#         cluster = Clusters(middle_wake_up_time=time(6, 30))
#         db.session.add(cluster)
#         db.session.commit()

#         # cluster_userモデルにテストデータを挿入
#         cluster_user_record = ClusterUser(user_id=user.id, cluster_id=cluster.id)
#         db.session.add(cluster_user_record)
#         db.session.commit()
        
#         pass

