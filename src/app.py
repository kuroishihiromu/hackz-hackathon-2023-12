from flask import Flask
from flask_migrate import Migrate

#自作のdatabaseモジュールをインポート
from database.models import *
from database.seeder import *
from database import init_db



app = Flask(__name__)

init_db(app) #環境変数の設定
db.init_app(app) #DBの初期化
migrate = Migrate(app, db) #マイグレーションの設定


@app.route('/')
def hello():
    # db.create_all()
    # database_seeder(app)
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)




#テスト用のデータを一括挿入する。
def db_seeder():
    from faker import Faker
    import random
    
    faker = Faker('ja_JP')
    users = []
    
    for _ in range(100):
        user = User(
            device_id = faker.random_number(digits=12),
            name = faker.name(),
            email = faker.email(),
            password = faker.password(),
            is_bot = random.choice([True, False])
        )
        users.append(user)

    # 一度にすべてのユーザーを保存
    db.session.bulk_save_objects(users)
    db.session.commit()
