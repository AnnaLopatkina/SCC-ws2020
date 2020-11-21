from flask import render_template, redirect, url_for, flash, session, request, jsonify, abort
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy.orm import query

from clientManager.entities import User, Study
from clientManager import app, db
from clientManager.inputforms import LoginForm, RegistrationForm, ProfileForm
import requests

service_ip = "localhost"
service_port = "5000"
headers = {
    "Accept-Encoding": "gzip",
    "User-Agent": "Web-Client"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def login2():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nutzername oder Passwort falsch')
            return redirect(url_for('login'))

        login_user(user, True)
        session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET'])
def register():
    form = RegistrationForm()

    return render_template('register.html', form=form)


@app.route('/register', methods=['POST'])
def register_post():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    url = "http://{}:{}/test/api/studies".format(service_ip, service_port)
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    user = User.query.filter_by(id=current_user.id).first()

    if user.study:
        form = ProfileForm(studies=user.study)

    else:
        form = ProfileForm()

    form.email.data = user.email
    form.name.data = user.username
    form.studies.choices = [(study["id"], study["title"]) for study in r.json()["studies"]]

    return render_template('profileedit.html', form=form)


@app.route('/profile', methods=['POST'])
@login_required
def profileedit():

    form = ProfileForm()
    if form.validate_on_submit():

        user = User.query.filter_by(id=current_user.id).first()

        if Study.query.filter_by(id=form.studies.data).first() is not None:

            user.study = Study.query.filter_by(id=form.studies.data).first().id
        else:
            print('study not in local db yet')
            url = "http://{}:{}/test/api/studies".format(service_ip, service_port)
            r = requests.get(url=url, headers=headers)
            if r.status_code != 200:
                print("request failed with status: {}".format(r.status_code))

            study = Study()
            study.id = [study for study in r.json()["studies"] if study['id'] == form.studies.data][0]['id']
            study.title = [study for study in r.json()["studies"] if study['id'] == form.studies.data][0]['title']

            db.session.add(study)

            user.study = study.id
            db.session.add(user)
            db.session.commit()

        user.username = form.name.data
        user.email = form.email.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profile'))

    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('index'))


@app.route('/test/api/studies', methods=['GET'])
def testapi1():
    return jsonify({
        "studies": [
            {
                "id": "1",
                "title": "Bachelor Informatik"
            },
            {
                "id": "2",
                "title": "Diplom Informatik"
            },
            {
                "id": "3",
                "title": "Master Informatik"
            }
        ]
    })


@app.route('/test/api/study/<int:study_id>', methods=['GET'])
def testapi(study_id):
    return jsonify({"id": "1", "title": "Bachelor Informatik"})
