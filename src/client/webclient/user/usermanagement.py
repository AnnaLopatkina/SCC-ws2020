from functools import wraps

import requests
from flask import flash, redirect, url_for, session
from flask_login import current_user

from webclient import db, loginmanager
from webclient.config import service_ip, userservice_port, api_version, headers
from webclient.study.studymanagement import getstudies
from webclient.user.forms import ProfileForm
from webclient.user.models import Role, User


def register_user(username, email, password):
    url = "http://{}:{}/{}/registerUser".format(service_ip, userservice_port, api_version)
    r = requests.put(url=url, headers=headers, json={'name': username, 'email': email, 'password': password})
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def getToken(email, password):
    url = "http://{}:{}/{}/loginToken".format(service_ip, userservice_port, api_version)
    r = requests.post(url=url, headers=headers, json={'email': email, 'password': password})
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def check_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash("You need to log in to view this page.")
            return redirect(url_for('index'))

    return wrap


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if session['is_admin']:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for('index'))

    return wrap


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


def createprofileform(user_id):
    r = getstudies()

    user = getUser(user_id)

    if user.json()['study']:
        form = ProfileForm(studies=user.json()['study'], roles=user.json()['roles'])

    else:
        form = ProfileForm()

    form.user_id.data = user.json()['id']
    form.email.data = user.json()['email']
    form.name.data = user.json()['username']
    form.semester.data = user.json()['semester']
    form.studies.choices = [(int(study["id"]), study["title"]) for study in r.json()["studies"]]
    form.roles.choices = [(int(role['id']), role['name']) for role in getRoles().json()['roles']]
    form.roles.data = str(user.json()['roles'][0]['id'])

    return form


def createstudychoices():
    r = getstudies()
    return [(study["id"], study["title"]) for study in r.json()["studies"]]


def getUser(user_id):
    url = "http://{}:{}/{}/user/{}".format(service_ip, userservice_port, api_version, user_id)

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['token']

    r = requests.get(url=url, headers=headers_token)
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def getRoles():
    url = "http://{}:{}/{}/getRoles".format(service_ip, userservice_port, api_version)

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['token']

    r = requests.get(url=url, headers=headers_token)
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def submit_user(user_id, passwordold, passwordnew, username, email, semester, role_id, study_id):
    url = "http://{}:{}/{}/editUser".format(service_ip, userservice_port, api_version)

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['token']

    user = {
        'id': user_id,
        'passwordold': passwordold,
        'passwordnew': passwordnew,
        'username': username,
        'email': email,
        'semester': semester,
        'role': role_id,
        'study': study_id
    }

    r = requests.put(url=url, headers=headers_token, json=user)

    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r