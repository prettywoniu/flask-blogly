"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

# MODELS GO BELOW #
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(30), 
                           nullable=False)
    last_name = db.Column(db.String(30), 
                          nullable=False)
    img_url = db.Column(db.String)

class Post(db.Model):
    
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, 
                      nullable=False)
    content = db.Column(db.String(500))
    # ??? what is the best way to show date + time
    created_at = db.Column(db.DateTime, 
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)
    
    user = db.relationship('User', backref='posts')
