

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from cluster_manager import ClusterManager
from flask_cors import CORS
from tree_manager import TreeManager
import json
import pickle

#自作のdatabaseモジュールをインポート
from database.models import *
from database.seeder import *
from database import init_db

from werkzeug.security import check_password_hash


app = Flask(__name__)

CORS(app)
app.config['SECRET_KEY'] ='your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

init_db(app) #環境変数の設定
db.init_app(app) #DBの初期化
migrate = Migrate(app, db) #マイグレーションの設定


@app.route('/')
def index():
    return "hello"

@app.route('/seed/<num>', methods=['GET'])
def seeder(num):
    n = int(num)
    database_seeder(app,n)
    return num + '件のダミーデータを挿入しました。'

# 定期実行デーモンからの依頼を受けて、クラスターを作成、保存したのち、各クラスターのルートユーザーのidとその起床時刻をjson形式で返す。
@app.route('/create_cluster')
def create_cluster():
    cluster_manager = ClusterManager(app)
    cluster_manager.init_cluster()
    
    # tree_manager = TreeManager(cluster_manager.clusters[0])
    # tree_manager.create_tree()
    
    tree_managers = []
    dict = {}
    for cluster in cluster_manager.clusters:
        tree_manager = TreeManager(cluster)
        tree_manager.create_tree()
        tree_managers.append(tree_manager)
        dict[tree_manager.root_user.id] = str(cluster.middle_wake_up_time)

    # 今日の日付
    today = datetime.now().strftime('%Y%m%d')
    
    # バイナリとして保存
    with open('./tree_logs/{}_trees.pkl'.format(today), 'wb') as file:
        pickle.dump(tree_managers, file)   
    
    return jsonify(dict)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if'username' not in data or 'password' not in data:
        return jsonify({'error':'無効なリクエスト'}), 400
    
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'ログイン成功'})
    else:
        return jsonify({'error': '無効な資格情報'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if 'username' not in data or'password' not in data or 'DeviceID' not in data:
        return jsonify({'error': '無効なリクエスト'}), 400

    username = data['username']
    password = data['password']
    device_id = data['DeviceID']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error':'既に登録済みです。'}), 400
    
    new_user = User(username=username, password=password, device_id = device_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '登録されました。'})

if __name__ == '__main__':
    app.run(debug=True)

