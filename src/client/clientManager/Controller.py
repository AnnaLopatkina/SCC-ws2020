from flask import render_template, redirect, url_for, flash, session, request, jsonify, abort
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps

from clientManager.entities import User, Study, Role
from clientManager import app, db, loginmanager
from clientManager.inputforms import LoginForm, RegistrationForm, ProfileForm, StudyForm
import requests
from clientManager.config import *
from clientManager.studymanagement import getstudies, getstudy


@app.route("/studiesAdmin")
@login_required
def studies_admin():
    r = getstudies()
    print(r.json()['studies'])
    return render_template("studies_admin.html", studies=r.json()['studies'])


@app.route("/editStudy/<int:studyid>", methods=['GET'])
@login_required
def studies_edit_admin(studyid):
    r = getstudies()

    study = r.json()['studies'][studyid]
    form = StudyForm(studyid=studyid, title=study['title'], description=study['description'])

    return render_template('study_admin_edit.html', form=form)


@app.route("/editStudy/<int:studyid>", methods=['POST'])
@login_required
def studies_edit_admin_post(studyid):
    form = StudyForm()

    if form.validate_on_submit():
        study = {
            "id": form.studyid.data,
            "title": form.title.data,
            "description": form.description.data
        }

        url = "http://{}:{}/{}/study".format(service_ip, service_port, api_version)

        r = requests.put(url=url, headers=headers, json=study)
        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

    return redirect(url_for('studies_admin'))


@app.route("/addStudy", methods=['GET'])
@login_required
def studies_add_admin():
    form = StudyForm()
    return render_template('study_admin_edit.html', form=form)


@app.route("/addStudy", methods=['POST'])
@login_required
def studies_save_admin():
    form = StudyForm()

    if form.validate_on_submit():
        study = {
            "id": form.studyid.data,
            "title": form.title.data,
            "description": form.description.data
        }
        print("send study: {}".format(study))

        url = "http://{}:{}/{}/study".format(service_ip, service_port, api_version)

        r = requests.put(url=url, headers=headers, json=study)
        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

    return redirect(url_for('studies_admin'))


@app.route("/myStudy", methods=['GET'])
def mystudy():
    data = db.session.query(Study).join(User).filter(User.email == current_user.email).first()

    if data is None:
        return render_template("mystudy.html", error=True)

    r = getstudy(data.id)
    print(r.json())

    return render_template("mystudy.html", study=r.json(), user=current_user)