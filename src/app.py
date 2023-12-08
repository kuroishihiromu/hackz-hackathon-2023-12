from flask import Flask
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

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
            cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL)")
            print("テストテーブルを作成しました。")

            return connection

    except Error as e:
        print(f"データベース接続中にエラーが発生しました: {e}")
        return None
