# モデルのインポート
from datetime import time , datetime, timedelta
from .models import *
from faker import Faker
import random

def database_seeder(app,num):
    with app.app_context():
        
        faker = Faker('ja_JP')

        # 現在の日時を取得
        now = datetime.now()

        # 10日前の日時を計算
        ten_days_ago = now - timedelta(days=10)
        
        for _ in range(num):
            
            # 一人のユーザーを作成
            user = User(
                device_id = faker.random_number(digits=12),
                name = faker.name(),
                email = faker.unique.email(),
                password = "password"
            )
            db.session.add(user)
            db.session.commit()  # ユーザーごとにコミット
            
            # 一人のユーザーに対して過去10日分の設定を作成
            for i in range(10):
                # ランダムな時間を生成（5:00から12:00まで）
                random_hour = random.randint(5, 11)
                random_minute = random.randint(0, 59)
                random_time = time(random_hour, random_minute)

                # 設定された日時を計算
                setting_at = ten_days_ago + timedelta(days=i)

                setting = Settings(
                    user_id = user.id,
                    tomorrow_wake_up_time = random_time,
                    yesterday_sleep_level = random.randint(1, 5),
                    setting_at = setting_at
                )
                db.session.add(setting)
                
        db.session.commit()
        

