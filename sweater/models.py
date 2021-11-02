from flask_login import UserMixin

from sweater import db, manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    pass_img = db.Column(db.String(255), nullable=False)
    counter = db.Column(db.Integer, default=0)
    coordinates = db.Column(db.String(128))
    banned = db.Column(db.Integer, default=0)
    false_click_counter = db.Column(db.Integer, default=0)
    zone = db.Column(db.String(512))
    probability = db.Column(db.String(512))


class Image(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# @manager.user_loader
# def load_user(user_id):
#     return None