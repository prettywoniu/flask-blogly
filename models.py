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
    assignments = db.relationship('PostTag', backref='posts')
    # tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')
    assignments = db.relationship('PostTag', backref='tags')

class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey("tags.id"),
                       primary_key=True)