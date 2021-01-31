from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
                                        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sa>dyfxghcjvhkbjlkiö'
db = SQLAlchemy(app)

import userService.routes

db.create_all()


