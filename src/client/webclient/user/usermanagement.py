from functools import wraps

import requests
from flask import flash, redirect, url_for, session

from webclient.config import service_ip, userservice_port, api_version, headers
from webclient.study.studymanagement import getstudies
from webclient.user.forms import ProfileForm


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


def setStudyToken(token):

    url = "http://{}:{}/{}/setStudyToken/{}".format(service_ip, userservice_port, api_version, session['id'])

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['token']

    r = requests.put(url=url, headers=headers, json={'study_token': token})
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def create_role(name):
    url = "http://{}:{}/{}/addRole".format(service_ip, userservice_port, api_version)

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['token']

    r = requests.put(url=url, headers=headers, json={'name': name})
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


def createprofileform(user_id):
    r = getstudies()

    user = getUser(user_id)

    if user.json()['study_id']:
        form = ProfileForm(studies=user.json()['study_id'], roles=user.json()['roles'])

    else:
        form = ProfileForm()

    form.user_id.data = user.json()['id']
    form.email.data = user.json()['email']
    form.name.data = user.json()['username']
    form.semester.data = user.json()['semester']
    form.studies.choices = [(int(study["id"]), study["title"]) for study in r.json()["studies"]]
    form.roles.choices = [(int(role['id']), role['name']) for role in get_roles().json()['roles']]
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


def find_all_users():
    url = "http://{}:{}/{}/users".format(service_ip, userservice_port, api_version)

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['token']

    r = requests.get(url=url, headers=headers_token)
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def get_roles():
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

    study_title = ''

    studies = getstudies()
    for study in studies.json()['studies']:
        if study['id'] == study_id:
            study_title = study['title']

    user = {
        'id': user_id,
        'passwordold': passwordold,
        'passwordnew': passwordnew,
        'username': username,
        'email': email,
        'semester': semester,
        'role': role_id,
        'study': {
            'id': study_id,
            'title': study_title
        }
    }

    r = requests.put(url=url, headers=headers_token, json=user)

    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r

