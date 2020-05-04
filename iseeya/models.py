from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from iseeya import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    iwanna = db.relationship('Iwanna', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @staticmethod
    def verify_stream_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            s.loads(token).get('user_id')
            return True
        except:
            return False

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    cover = db.relationship('Cover', backref='page', lazy=True)
    items = db.relationship('Item', backref='page', lazy=True)
    sub_items = db.relationship('SubItem', backref='page', lazy=True)
    contentt = db.relationship('Content', backref='page', lazy=True)

class Cover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(100))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(100))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)

class SubItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(100))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)


class Iwanna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
