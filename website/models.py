from sqlalchemy.orm import backref
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(150), unique = True)
    name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # membuat relationship one to Many ke table Posts
    posts = db.relationship('Posts', backref='user', passive_deletes=True)
    

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Text, nullable=False)
    # membuat foreign key untuk id user penulis
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())