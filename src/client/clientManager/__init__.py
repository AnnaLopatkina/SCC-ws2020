from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, current_user

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
                                        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dsuiafohu0o437tzghsrodinzt478oemsfuhidohsguieo'
db = SQLAlchemy(app)
loginmanager = LoginManager(app)

import clientManager.Controller
import clientManager.api_controller

db.create_all()