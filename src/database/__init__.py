from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://user:password@db:3306/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

