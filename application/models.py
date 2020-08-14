from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from application import db, login

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
                     )


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(128))
    about = db.Column(db.String(150))
    last_seen = db.Column(db.String(100), index=True, unique=True)
    posts = db.relationship('Posts', backref='author', lazy='dynamic')
    followed = db.relationship('Users', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.username)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def avatar(self, size):
        hashed_email = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(hashed_email, size)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    # followers functionality implementation
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        flwd_posts = Posts.query.join(followers, (followers.c.followed_id == Posts.user_id)).filter(
            followers.c.follower_id == self.id)
        own_posts = Posts.query.filter_by(Posts.user_id == self.id)
        return flwd_posts.union(own_posts).order_by(Posts.timestamp.desc())


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
