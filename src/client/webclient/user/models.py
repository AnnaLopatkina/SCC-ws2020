from flask_login import UserMixin
from flask_sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash

from webclient import db, loginmanager
from webclient.config import admin_email, admin_password, admin_username


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return self.name


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

    def is_authenticated(self):
        return True

    def set_role(self, role):
        self.roles.append(role)

    def get_roles(self):
        return self.roles

    def get_role_string(self):
        rolestring = ""
        for role in self.get_roles():
            if rolestring != "":
                rolestring += ', '
            rolestring += role.name
        return rolestring

    def is_admin(self):
        for role in self.roles:
            if role.name == "ADMIN":
                return True
        return False

    def has_role(self, rolestring):
        for role in self.roles:
            if role.name == rolestring:
                return True
        return False

    @classmethod
    def users_full(cls):
        return User.query.join(Study).all()


@event.listens_for(User.__table__, 'after_create')
def create_admin_and_roles(*args, **kwargs):
    print("init admin user & roles")

    admin = User(admin_username, admin_email)
    admin.set_password(admin_password)

    db.session.add(admin)
    db.session.commit()


@event.listens_for(Role.__table__, 'after_create')
def create_roles(*args, **kwargs):
    admin_role = Role()
    admin_role.name = "ADMIN"

    student_role = Role()
    student_role.name = "STUDENT"

    db.session.add(admin_role)
    db.session.add(student_role)
    db.session.commit()


@event.listens_for(UserRoles.__table__, 'after_create')
def admin_role(*args, **kwargs):
    admin_r = Role.query.filter_by(name="ADMIN").first()
    admin = User.query.filter_by(email=admin_email).first()
    admin.set_role(admin_r)

    db.session.add(admin)
    db.session.commit()


@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
