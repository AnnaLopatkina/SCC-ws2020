import requests
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from webclient import app, db
from webclient.config import *
from webclient.study.studymanagement import getstudies, getstudy
from webclient.study.forms import StudyForm, ModuleForm
from webclient.user.models import User
from webclient.study.models import Study
from webclient.user.usermanagement import login_required_and_roles


@app.route("/studiesAdmin")
@login_required_and_roles(role="ADMIN")
def studies_admin():
    r = getstudies()
    print(r.json()['studies'])
    return render_template("studies_admin.html", studies=r.json()['studies'])


@app.route("/editStudy/<int:studyid>", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def studies_edit_admin(studyid):
    r = getstudies()

    study = r.json()['studies'][studyid]
    form = StudyForm(studyid=studyid, title=study['title'], description=study['description'])

    return render_template('study_admin_edit.html', form=form)


@app.route("/editStudy/<int:studyid>", methods=['POST'])
@login_required_and_roles(role="ADMIN")
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
@login_required_and_roles(role="ADMIN")
def studies_add_admin():
    form = StudyForm()
    return render_template('study_admin_edit.html', form=form)


@app.route("/addStudy", methods=['POST'])
@login_required_and_roles(role="ADMIN")
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
@login_required
def mystudy():
    data = db.session.query(Study).join(User).filter(User.email == current_user.email).first()

    if data is None:
        return render_template("mystudy.html", error=True)

    r = getstudy(data.id)
    print(r.json())

    return render_template("mystudy.html", study=r.json(), user=current_user)


@app.route("/study/<int:studyid>/addModule", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def add_module(studyid):
    study = getstudy(studyid)
    form = ModuleForm()

    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>/addModule", methods=['POST'])
@login_required_and_roles(role="ADMIN")
def add_module_post(studyid):
    form = ModuleForm()
    study = getstudy(studyid)

    print(form.validate())
    print(form.errors)

    if form.validate_on_submit():
        module = {
            "studyid": studyid,
            "id": "",
            "title": form.title.data,
            "short": form.short.data,
            "description": form.description.data,
            "duration": form.duration.data,
            "credits": form.credits.data,
            "responsible": form.responsible.data,
            "teaching": form.teaching.data,
        }

        # add api put request here
        print(module)

        url = "http://{}:{}/{}/study/{}/module".format(service_ip, service_port, api_version, studyid)

        r = requests.put(url=url, headers=headers, json=module)
        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

        return redirect(url_for('studies_admin'))

    return render_template("editModule.html", form = form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>/editModule/<int:moduleid>", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def edit_module(studyid, moduleid):
    study = getstudy(studyid)
    form = ModuleForm()

    studyjson = study.json()
    print(studyjson)

    for module in study.json()['study']["modules"]:
        print("check module id {} if it equals {} ? {}".format(module['id'], moduleid, int(module['id']) == moduleid))
        if int(module['id']) == moduleid:
            print("set values")
            form.moduleid.data = module['id']
            form.title.data = module['title']
            form.short.data = module['short']
            form.description.data = module['description']
            form.duration.data = module['duration']
            form.credits.data = module['credits']
            form.responsible.data = module['responsible']
            form.teaching.data = module['teaching']


    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>/editModule/<int:moduleid>", methods=['POST'])
@login_required_and_roles(role="ADMIN")
def edit_module_post(studyid, moduleid):
    form = ModuleForm()
    study = getstudy(studyid)

    if form.validate_on_submit():
        module = {
            "title": form.title.data,
            "short": form.short.data,
            "description": form.description.data,
            "duration": form.duration.data,
            "credits": form.credits.data,
            "responsible": form.responsible.data,
            "teaching": form.teaching.data,
        }

        print(module)

        # add api put request here

        return redirect(url_for('studies_admin'))

    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())

























