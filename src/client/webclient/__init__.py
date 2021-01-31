import os

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsuiafohu0o437tzghsrodinzt478oemsfuhidohsguieo'

import webclient.study.routes
import webclient.user.routes