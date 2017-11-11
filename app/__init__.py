import os
from flask_login import LoginManager
from flask_navigation import Navigation
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'images/')

app = Flask(__name__)
nav = Navigation(app)

app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/main'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(UPLOAD_FOLDER)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.views import loginView
from app.views import goodsView
from app.views import view
from app.views import imageView

from app.models import Users
