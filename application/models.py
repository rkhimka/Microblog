from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from application import db, login


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(128))
    about = db.Column(db.String(150))
    last_seen = db.Column(db.String(100), index=True, unique=True)
    posts = db.relationship('Posts', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.username)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def avatar(self, size):
        hashed_email = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(hashed_email, size)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Post {}>".format(self.body)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
