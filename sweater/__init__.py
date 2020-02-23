import os.path
import tempfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'two-factor authorization salt'
app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
#manager.login_view = 'login_page'

from sweater import models, routes

db.create_all()
