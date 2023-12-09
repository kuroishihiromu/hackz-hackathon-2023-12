# モデルのインポート
from datetime import time, timedelta
from .models import *
from faker import Faker
import random

def database_seeder(app):
    with app.app_context():
        
        faker = Faker('ja_JP')
        users = []
        
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
            settings = []
            for i in range(10):
                # 開始時間と終了時間を定義
                start_time = time(5, 30)
                end_time = time(12, 0)

                # ランダムな時間を生成
                random_minutes = random.randint(0, (end_time.hour - start_time.hour) * 60 + (end_time.minute - start_time.minute))
                random_time = start_time + timedelta(minutes=random_minutes)
                
                setting = Settings(
                    user_id = user.id,
                    tomorrow_wake_up_time = random_time,
                    yesterday_sleep_level = random.randint(1, 3)
                )
            
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

