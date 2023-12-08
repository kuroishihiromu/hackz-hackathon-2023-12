from flask import Flask
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import Error
from datetime import datetime
import os


app = Flask(__name__)

# connect to database ##
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@db:3306/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#make SQLObject
db = SQLAlchemy(app)

class settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tomorrow_wake_up_time = db.Column(db.Time, nullable=False)
    yesterday_sleep_level = db.Column(db.Integer,nullable=False)
    setting_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    device_id = db.Column(db.VARCHAR(12),nullable=False,unique= True)
    name = db.Column(db.VARCHAR(24),nullable=False)
    email = db.Column(db.VARCHAR(24),nullable=False,unique= True)
    password = db.Column(db.VARCHAR(12),nullable=False)
    is_bot = db.Column(db.Boolean, default=True,nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

class cluster_user(db.Model):
    __tablename__ = 'cluster_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

class clusters(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    middle_wake_up_time = db.Column(db.Time, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())




@app.route('/')
def hello_hiromu():
    return 'Hello, asdhiromu!'

@app.route('/test')
def hello_tomokazu():
    # 関数の使用例
    DB_HOST = 'db'
    DB_PORT = 3306
    DB_DATABASE = 'mydatabase'
    DB_USERNAME = 'user'
    DB_PASSWORD = 'password'

    connection = connect_to_database(DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD)

    return 'Hello, tomokazu!'

def connect_to_database(host, port, database, username, password):
    """MySQLデータベースへの接続を試み、接続オブジェクトを返す。同時にテストテーブルを作成する。"""
    try:
        # データベース接続の確立
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )

        if connection.is_connected():
            print(f"MySQLサーバーに接続しました: {connection.get_server_info()}")

            # テストテーブルの作成
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT autoincrement PRIMARY KEY, name VARCHAR(255) NOT NULL)")
            print("テストテーブルを作成しました。")

            return connection

    except Error as e:
        print(f"データベース接続中にエラーが発生しました: {e}")
        return None
