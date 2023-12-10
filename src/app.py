from flask import Flask
from flask_migrate import Migrate
from cluster_manager import ClusterManager
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
    return 'Hello, World!'

@app.route('/seed/<num>', methods=['GET'])
def seeder(num):
    n = int(num)
    database_seeder(app,n)
    return num + '件のダミーデータを挿入しました。'

@app.route('/cluster')
def create_cluster():
    manager = ClusterManager(app)
    manager.init_cluster()
    return manager.get_cluster_info()

if __name__ == '__main__':
    app.run(debug=True)

