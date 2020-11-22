from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from clientManager import db, login


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    semesters = db.Column(db.Integer(), primary_key=False)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(99), nullable=False)
    email = db.Column(db.String(99), unique=True, nullable=False)
    password_hash = db.Column((db.String(250)))
    semester = db.Column(db.Integer(), primary_key=False)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    study = db.Column(db.Integer, db.ForeignKey('study.id'))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_study(self, studyid):
        self.study = studyid

    def get_study(self):
        return self.study

    @classmethod
    def users_full(cls):
        return User.query.join(Study).all()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
