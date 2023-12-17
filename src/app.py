

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from cluster_manager import ClusterManager
from flask_cors import CORS
from tree_manager import TreeManager
from aws_manager import AwsManager
import json
import pickle

import os
import glob
from datetime import datetime

#自作のdatabaseモジュールをインポート
from database.models import *
from database.seeder import *
from database import init_db

from werkzeug.security import check_password_hash


app = Flask(__name__)

CORS(app, origin="http://localhost:8000")
app.config['SECRET_KEY'] ='your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

init_db(app) #環境変数の設定
db.init_app(app) #DBの初期化
migrate = Migrate(app, db) #マイグレーションの設定
# socketio = SocketIO(app)

@app.route('/')
def index():
    return "hello"

@app.route('/aws')
def aws():
    aws_manager = AwsManager()
    aws_manager.create_wake_up_rule()
    return "finished!"

@app.route('/wake_up/<index>', methods=['GET'])
def test(index):
    
    # 今日の日付
    today = datetime.now().strftime('%Y%m%d')
    
    # 指定された日付のファイルを検索
    file_pattern = "./tree_logs/{}_trees_*.pkl".format(today)
    file_list = glob.glob(file_pattern)

    # ファイルが存在する場合、最新のファイルを見つける
    if file_list:
        latest_file = max(file_list, key=os.path.getmtime)
        print(f"Using the latest file: {latest_file}")

        # 最新のファイルからtree_managersを読み込む
        with open(latest_file, 'rb') as f:
            loaded_object = pickle.load(f)
    else:
        print(f"No files found for pattern: {file_pattern}")
        # 適切なエラーハンドリングか、デフォルトの動作をここに記述
    
    # loaded_object[int(index)].wake_up_child(loaded_object[int(index)].root_user)
    user_id = loaded_object[int(index)-1].root_user_id
    proces_id = loaded_object[int(index)-1].start_threading_process(user_id)
    
    return jsonify({
        'message': '正常に実行されました。',
        'process_id': proces_id
    })

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
    
    tree_managers = []
    tree_index = 1
    wake_up_rules = {}
    for cluster in cluster_manager.clusters:
        tree_manager = TreeManager(cluster)
        tree_manager.create_tree(int(tree_index))
        tree_managers.append(tree_manager)
        wake_up_rules[tree_index] = str(cluster.middle_wake_up_time)
        tree_index += 1
    
    # 新しい辞書を作成
    formatted_wake_up_rules = []
    for index, time in wake_up_rules.items():
        formatted_wake_up_rules.append({
            "tree_index": str(index),
            "set_time": time
        })
        
    # JSONに変換
    json_wake_up_rules = json.dumps(formatted_wake_up_rules)
    
    # 今日の日付
    today = datetime.now().strftime('%Y%m%d')
    current_time = datetime.now().strftime('%H%M%S')
    
    # ファイル名に日付と時刻を追加
    filename = './tree_logs/{}_trees_{}.pkl'.format(today, current_time)

    # バイナリとしてファイルに保存
    with open(filename, 'wb') as file:
        pickle.dump(tree_managers, file)
        
    # # awsにデータを送信し、新規ルールを定義
    # aws_manager = AwsManager()
    # aws_manager.create_wake_up_rule(wake_up_rules)
    
    return jsonify({
        'message': '正常に実行されました。',
        'rules': formatted_wake_up_rules
    })





@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()

    if'username' not in data or 'password' not in data:
        return jsonify({'error':'無効なリクエスト'}), 400
    
    email = data['username']
    password = data['password']

    user = User.query.filter(User.email == email).first()

    if user and user.password == password:
        return jsonify({'userid': user.id})
    else:
        return jsonify({'error': '無効な資格情報'}), 401
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if 'username' not in data or'password' not in data or 'DeviceID' not in data or 'Email' not in data:
        return jsonify({'error': '無効なリクエスト'}), 400

    existing_user = User.query.filter(User.email == data["Email"]).first()
    if existing_user:
        return jsonify({'error':'既に登録済みです。'}), 400

    new_user = User(
        name=data['username'], 
        password=data['password'], 
        email=data['Email'],
        device_id = data['DeviceID']  
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'userid': new_user.id})

@app.route('/set_time', methods=['POST'])
def set_time():
    data = request.get_json()
    settingTime = Settings(
        user_id = data['user_id'],
        tomorrow_wake_up_time = data['WakeUpTime'],
        yesterday_sleep_level = data['SleepLevel']
    )
    db.session.add(settingTime)
    db.session.commit()

    return jsonify({'success':True})

# nodes =[
#     {"node_id": 1, "user_id": 1, "name":"Node1","wakeup":False,"created_at":"2023-01-01"},
# ]

# @socketio.on('update_node_wakeup')
# def handle_update_node_wakeup(data):
#     node_id = data["node_id"]
#     wakeup = data["wakeup"]

#     for node in nodes:
#         if node["node_id"] == node_id:
#             node["wakeup"] = wakeup
#             break
    
#     socketio.emit("node_wakeup_updated",{"node_id":node_id,"wakeup":wakeup})



@app.route('/tree_state', methods=['POST'])
def tree_state():

    data = request.get_json()
    user_id = int(data['user_id'])
    
    # 今日の日付 
    today = datetime.now().strftime('%Y%m%d')
    
    # 指定された日付のファイルを検索
    file_pattern = "./tree_logs/{}_trees_*.pkl".format(today)
    file_list = glob.glob(file_pattern)

    # ファイルが存在する場合、最新のファイルを見つける
    if file_list:
        latest_file = max(file_list, key=os.path.getmtime)
        print(f"Using the latest file: {latest_file}")

        # 最新のファイルからtree_managersを読み込む
        with open(latest_file, 'rb') as f:
            loaded_object = pickle.load(f)
    else:
        print(f"No files found for pattern: {file_pattern}")
        
    for tree_manager in loaded_object:
        print(tree_manager.user_id_list)
        if user_id in tree_manager.user_id_list:
            break
    
    # ルートノードの情報を取得
    return tree_manager.get_tree_state()

# @app.route('/tree_state_test/<user_id>', methods=['GET'])
# def tree_state_test(user_id):

    
#     # 今日の日付
#     today = datetime.now().strftime('%Y%m%d')
    
#     # 指定された日付のファイルを検索
#     file_pattern = "./tree_logs/{}_trees_*.pkl".format(today)
#     file_list = glob.glob(file_pattern)

#     # ファイルが存在する場合、最新のファイルを見つける
#     if file_list:
#         latest_file = max(file_list, key=os.path.getmtime)
#         print(f"Using the latest file: {latest_file}")

#         # 最新のファイルからtree_managersを読み込む
#         with open(latest_file, 'rb') as f:
#             loaded_object = pickle.load(f)
#     else:
#         print(f"No files found for pattern: {file_pattern}")
        
#     for tree_manager in loaded_object:
#         if user_id in tree_manager.user_id_list:
#             break
    
#     # ルートノードの情報を取得
    
#     return str("asdfadf")
    
    


@app.route('/get_depth_level/<device_id>', methods=['GET'])
def get_depth_level(device_id):
    user = User.query.filter(User.device_id == device_id).first()
    
    # ユーザーが所属するクラスターの中で最新のものを取得
    # cluster_id = user.clusters.order_by(ClusterUser.create_at.desc()).first().cluster_id
    cluster_id = db.session.query(ClusterUser).filter_by(user_id=user.id).order_by(ClusterUser.create_at.desc()).first().id
    
    # cluster_idをもとに、tree_indexを取得
    
    # 今日の日付
    today = datetime.now().strftime('%Y%m%d')
    
    # 指定された日付のファイルを検索
    file_pattern = "./tree_logs/{}_trees_*.pkl".format(today)
    file_list = glob.glob(file_pattern)

    # ファイルが存在する場合、最新のファイルを見つける
    if file_list:
        latest_file = max(file_list, key=os.path.getmtime)
        print(f"Using the latest file: {latest_file}")

        # 最新のファイルからtree_managersを読み込む
        with open(latest_file, 'rb') as f:
            loaded_object = pickle.load(f)
    else:
        print(f"No files found for pattern: {file_pattern}")
        
    for tree_manager in loaded_object:
        if cluster_id == tree_manager.cluster_id:
            break
    
    
    return jsonify({
        'depth_level'
        : Process.query.filter(Process.process_id == tree_manager.process_id).order_by(Process.create_at.desc()).first().depth_level
    })
    
if __name__ == '__main__':
    app.run(debug=True)

