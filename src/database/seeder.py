from datetime import time, datetime, timedelta
from .models import *
from faker import Faker
import random

def database_seeder(app, num):
    with app.app_context():
        faker = Faker('ja_JP')
        now = datetime.now()
        ten_days_ago = now - timedelta(days=10)

        users = []
        settings = []

        for _ in range(num):
            # 一意性を確保するための追加ロジックが必要です
            user = User(
                device_id=faker.random_number(digits=12),
                name=faker.name(),
                email=faker.unique.email(),
                password="password"
            )
            users.append(user)

        # ユーザーを一括で追加
        db.session.add_all(users)
        db.session.commit()

        for user in users:
            for i in range(10):
                random_hour = random.randint(5, 11)
                random_minute = random.randint(0, 59)
                random_time = time(random_hour, random_minute)
                setting_at = ten_days_ago + timedelta(days=i)

                setting = Settings(
                    user_id=user.id,
                    tomorrow_wake_up_time=random_time,
                    yesterday_sleep_level=random.randint(1, 5),
                    setting_at=setting_at
                )
                settings.append(setting)

        # 設定を一括で追加
        db.session.add_all(settings)
        db.session.commit()
