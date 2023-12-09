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
    database_seeder(app)
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

