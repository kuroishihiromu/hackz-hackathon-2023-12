from flask import Flask
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import Error
from datetime import datetime
import os


app = Flask(__name__)

# connect to database ##
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://user:password@db:3306/mydatabase'
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

class groupe_user(db.Model):
    __tablename__ = 'groupe_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

class groupes(db.Model):
    __tablename__ = 'groupes'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    middle_wake_up_time = db.Column(db.Time, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())


@app.route('/')
def hello():
    db.create_all()
    return 'Hello, World!'

