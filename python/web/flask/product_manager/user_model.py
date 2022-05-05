from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bb75acb5adb1a96ce3d491f0b2db5683'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://naren:Python123@192.168.161.128/classicmodels"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# connects Flask with SQlAlchemy ORM

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    


db.create_all()