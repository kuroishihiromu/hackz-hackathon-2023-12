

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from cluster_manager import ClusterManager
from flask_cors import CORS
from tree_manager import TreeManager
from aws_manager import AwsManager
import json
import pickle
from flask_socketio import SocketIO

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
socketio = SocketIO(app)

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
    
    # piklからtree_managersを読み込み
    with open("./tree_logs/{}_trees.pkl".format(today), 'rb') as f:
        loaded_object = pickle.load(f)
    
    # loaded_object[int(index)].wake_up_child(loaded_object[int(index)].root_user)
    user_id = loaded_object[int(index)].root_user_id
    proces_id = loaded_object[int(index)].start_threading_process(user_id)
    
    return {
        'statusCode': 200,  # HTTPステータスコード
        'headers': {  # 必要に応じてHTTPヘッダーを設定
            'Content-Type': 'application/json'
        },
        '': {
            
        },
        'body': json.dumps({  # レスポンス本文
            'message': '正常に実行されました。'
        })
    }

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
    tree_index = 0
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
    
    # バイナリとして保存 TODO:時刻をつけて、その日の最新版が使われるように
    with open('./tree_logs/{}_trees.pkl'.format(today), 'wb') as file:
        pickle.dump(tree_managers, file)  
        
    # # awsにデータを送信し、新規ルールを定義
    # aws_manager = AwsManager()
    # aws_manager.create_wake_up_rule(wake_up_rules)
    
    
    return {
        'statusCode': 200,  # HTTPステータスコード
        'headers': {  # 必要に応じてHTTPヘッダーを設定
            'Content-Type': 'application/json'
        },
        'rules':json_wake_up_rules,
        'body': json.dumps({  # レスポンス本文
            'message': '正常に実行されました。'
        })
    }



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

nodes =[
    {"node_id": 1, "user_id": 1, "name":"Node1","wakeup":False,"created_at":"2023-01-01"},
]

@socketio.on('update_node_wakeup')
def handle_update_node_wakeup(data):
    node_id = data["node_id"]
    wakeup = data["wakeup"]

    for node in nodes:
        if node["node_id"] == node_id:
            node["wakeup"] = wakeup
            break
    
    socketio.emit("node_wakeup_updated",{"node_id":node_id,"wakeup":wakeup})


if __name__ == '__main__':
    socketio.run(app, debug=True)

