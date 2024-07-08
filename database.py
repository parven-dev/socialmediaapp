from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt


from Main import app, db

Base = declarative_base()
bcrypt = Bcrypt(app)


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String, unique=True)
    email = Column(db.String, unique=True)
    password = Column(String)
    fullname = Column(String)
    profile_picture = Column(db.String(150), nullable=True)
    posts = db.relationship("Post", backref="authors", lazy=True)
    #one-to-many relationship with CommentDatabase

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String)
    subtitle = db.Column(db.String)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, nullable=False, default=datetime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    comments = db.relationship("CommentDatabase", backref="post", lazy=True)
    # one-to-many relationship with CommentDatabase


class CommentDatabase(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    today = db.Column(db.DateTime, nullable=False, default=datetime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(Integer, db.ForeignKey("posts.id"), nullable=False)
    author = db.relationship("Users", backref="comments", lazy=True)



with app.app_context():
    db.create_all()
