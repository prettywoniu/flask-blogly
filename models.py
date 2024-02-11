"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

# MODELS GO BELOW #
class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(30), 
                           nullable=False)
    last_name = db.Column(db.String(30), 
                          nullable=False)
    img_url = db.Column(db.String)
 