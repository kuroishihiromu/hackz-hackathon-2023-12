from flask import Flask
from flask_migrate import Migrate
from cluster_manager import ClusterManager
from flask_cors import CORS
#自作のdatabaseモジュールをインポート
from database.models import *
from database.seeder import *
from database import init_db



app = Flask(__name__)

CORS(app)
app.config['SECRET_KEY'] ='your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

init_db(app) #環境変数の設定
db.init_app(app) #DBの初期化
migrate = Migrate(app, db) #マイグレーションの設定


@app.route('/')
def hello():
    return "Hello! Yasetomo!"

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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful', 'username': user.name})
    else:
        return jsonify({'message': 'Login failed'})



if __name__ == '__main__':
    app.run(debug=True)

