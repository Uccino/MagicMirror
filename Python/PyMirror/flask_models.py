from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from webserver import db

# Model for the user
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

# Model for the posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.now)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    # Returns the object in an easily serializable format
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'posted': self.date_posted.strftime('%Y-%m-%d')
        }
