from . import db
from datetime import datetime, time

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tomorrow_wake_up_time = db.Column(db.Time, nullable=False)
    yesterday_sleep_level = db.Column(db.Integer,nullable=False)
    setting_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    device_id = db.Column(db.VARCHAR(12),nullable=False,unique= True)
    name = db.Column(db.VARCHAR(24),nullable=False)
    email = db.Column(db.VARCHAR(48),nullable=False,unique= True)
    password = db.Column(db.VARCHAR(12),nullable=False)
    is_bot = db.Column(db.Boolean, default=True,nullable=False)
    status = db.Column(db.Boolean, default=True,nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    
    # ユーザーに関連する設定（一対多のリレーションシップ）
    settings = db.relationship('Settings', backref='user', lazy=True)
    # ユーザーが属するクラスタ（多対多のリレーションシップ）
    clusters = db.relationship('Cluster', secondary='cluster_user', backref=db.backref('users', lazy='dynamic'))

class ClusterUser(db.Model):
    __tablename__ = 'cluster_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    middle_wake_up_time = db.Column(db.Time, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    
    # Userモデルで逆方向の関係性が既に定義済みなので、こちらは定義しない

class Process(db.Model):
    __tablename__ = 'processes'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    process_id = db.Column(db.Integer)
    depth_level = db.Column(db.Integer, default=0,nullable=False)
    tree_index = db.Column(db.Integer, nullable=True)
    status = db.Column(db.VARCHAR(12), default="waiting",nullable=False)
    termination_flag = db.Column(db.Boolean, default=False,nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    start_at = db.Column(db.DateTime, nullable=True)
    end_at = db.Column(db.DateTime, nullable=True)


