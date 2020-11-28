from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


from webclient import db, loginmanager
from webclient.study.studymanagement import getstudies
from webclient.user.forms import ProfileForm
from webclient.user.models import Role, User


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        for role in current_user.roles:
            if role.name == "Admin":
                return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for('index'))

    return wrap


def login_required_and_roles(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return loginmanager.unauthorized()
            if not (current_user.has_role(role)) and (role != "ANY"):
                return loginmanager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def add_role(user, rolestring):
    role = Role.query.filter_by(name=rolestring).first()
    print(role)
    if role is None:
        print("create new Role {}".format(rolestring))
        role = Role()
        role.name = rolestring
        db.session.add(role)

    print("add role to user")
    user.roles.append(role)

    db.session.add(user)
    db.session.commit()


def get_role(rolestring):
    role = Role.query.filter_by(name=rolestring).first()
    return role


def createprofileform(userid):
    r = getstudies()

    user = User.query.filter_by(id=userid).first()

    if user.study:
        form = ProfileForm(studies=user.study, roles=user.get_roles()[0])

    else:
        form = ProfileForm()

    form.email.data = user.email
    form.name.data = user.username
    form.semester.data = user.semester
    form.studies.choices = [(study["id"], study["title"]) for study in r.json()["studies"]]
    form.roles.choices = Role.query.all()

    return form


def createstudychoices():
    r = getstudies()
    return [(study["id"], study["title"]) for study in r.json()["studies"]]
