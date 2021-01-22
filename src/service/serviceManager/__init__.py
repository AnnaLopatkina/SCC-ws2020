from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
                                        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretKey'
db = SQLAlchemy(app)

token_username = "admin"
token_password = "superadmin"

import serviceManager.Controller

db.create_all()


