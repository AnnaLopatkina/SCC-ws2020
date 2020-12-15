import requests
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from requests.auth import HTTPBasicAuth

from webclient import app, db
from webclient.config import *
from webclient.study.forms import StudyForm, ModuleForm, LectureForm
from webclient.study.models import Study, Grade
from webclient.study.studymanagement import getstudies, getstudy
from webclient.user.models import User
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
    if current_user.api_token == '':
        return redirect(url_for("get_api_token"))

    r = getstudies()

    study = Study()

    for a in r.json()['studies']:
        if a['id'] == studyid:
            print('found study')
            study = a

    form = StudyForm(studyid=studyid, title=study['title'], description=study['description'], degree=study['degree'])

    return render_template('study_admin_edit.html', form=form)


@app.route("/editStudy/<int:studyid>", methods=['POST'])
@login_required_and_roles(role="ADMIN")
def studies_edit_admin_post(studyid):
    form = StudyForm()

    if form.validate_on_submit():
        study = {
            "id": form.studyid.data,
            "title": form.title.data,
            "description": form.description.data,
            "semesters": form.semesters.data,
            "degree": form.degree.data
        }

        url = "http://{}:{}/{}/study".format(service_ip, service_port, api_version)

        headers_token = headers
        headers_token["Authorization"] = "Bearer " + current_user.api_token

        r = requests.put(url=url, headers=headers_token, json=study)
        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

    return redirect(url_for('study_admin', studyid=studyid))


@app.route("/addStudy", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def studies_add_admin():
    if current_user.api_token == '':
        return redirect(url_for("get_api_token"))

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
            "description": form.description.data,
            "semesters": form.semesters.data,
            "degree": form.degree.data
        }
        print("send study: {}".format(study))

        url = "http://{}:{}/{}/study".format(service_ip, service_port, api_version)

        headers_token = headers
        headers_token["Authorization"] = "Bearer " + current_user.api_token

        r = requests.put(url=url, headers=headers_token, json=study)

        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

    return redirect(url_for('studies_admin'))


@app.route("/myGrades", methods=['GET'])
@login_required
def mygrades():
    data = db.session.query(Grade).filter(User.id == current_user.id)

    if data is None:
        return render_template("myGrades.html", error=True)

    return render_template("myGrades.html", user=current_user)


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
    if current_user.api_token == '':
        return redirect(url_for("get_api_token"))

    study = getstudy(studyid)
    form = ModuleForm()

    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>/addModule", methods=['POST'])
@login_required_and_roles(role="ADMIN")
def add_module_post(studyid):
    form = ModuleForm()

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
        headers_token = headers
        headers_token["Authorization"] = "Bearer " + current_user.api_token

        r = requests.put(url=url, headers=headers_token, json=module)

        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

        return redirect(url_for('study_admin', studyid=studyid))

    study = getstudy(studyid)
    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>/editModule/<int:moduleid>", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def edit_module(studyid, moduleid):
    if current_user.api_token == '':
        return redirect(url_for("get_api_token"))

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


@app.route("/study/<int:studyid>")
@login_required_and_roles(role="ADMIN")
def study_admin(studyid):
    study = getstudy(studyid)
    json = study.json()
    return render_template("study_admin.html", study=study.json())


# Lehrveranstaltungen verwalten

@app.route("/study/<int:studyid>/module/<int:moduleid>/addlecture", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def add_lecture(studyid, moduleid):
    if current_user.api_token == '':
        return redirect(url_for("get_api_token"))

    study = getstudy(studyid)
    form = LectureForm()

    return render_template("editLecture.html", form=form, title="Modul erstellen", study=study.json(), moduleid=moduleid)


@app.route("/study/<int:studyid>/module/<int:moduleid>/addlecture", methods=['POST'])
@login_required_and_roles(role="ADMIN")
def add_lecture_post(studyid, moduleid):
    form = LectureForm()
    study = getstudy(studyid)

    print(form.validate())
    print(form.errors)

    if form.validate_on_submit():
        lecture = {
            "moduleid": moduleid,
            "id": "",
            "title": form.title.data,
            "short": form.short.data,
            "description": form.description.data,
            "semester": form.semester.data,
            "responsible": form.responsible.data,
        }

        print(lecture)

        url = "http://{}:{}/{}/study/{}/module/{}/lecture".format(service_ip, service_port, api_version, studyid,
                                                                  moduleid)

        headers_token = headers
        headers_token["Authorization"] = "Bearer " + current_user.api_token

        r = requests.put(url=url, headers=headers_token, json=lecture)
        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

        return redirect(url_for('study_admin', studyid=studyid))

    return render_template("editLecture.html", form=form, title="Modul erstellen", study=study.json(), moduleid=moduleid)


@app.route("/study/<int:studyid>/module/<int:moduleid>/editLecture/<int:lectureid>", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def edit_lecture(studyid, moduleid, lectureid):
    if current_user.api_token == '':
        return redirect(url_for("get_api_token"))

    study = getstudy(studyid)
    form = LectureForm()

    studyjson = study.json()
    print(studyjson)

    for module in study.json()['study']["modules"]:
        print("check module id {} if it equals {} ? {}".format(module['id'], moduleid, int(module['id']) == moduleid))
        if int(module['id']) == moduleid:
            for lecture in module["lectures"]:
                if int(lecture['id']) == lectureid:
                    print("set values")
                    form.lectureid.data = lecture['id']
                    form.title.data = lecture['title']
                    form.short.data = lecture['short']
                    form.description.data = lecture['description']
                    form.semester.data = lecture['semester']
                    form.responsible.data = lecture['responsible']

    return render_template("editLecture.html", form=form, title=" Lehrveranstaltung bearbeiten", study=study.json(), moduleid=moduleid)


@app.route("/study/<int:studyid>/module/<int:moduleid>/editLecture/<int:lectureid>", methods=['POST'])
@login_required_and_roles(role="ADMIN")
def edit_lecture_post(studyid, moduleid, lectureid):
    form = LectureForm()
    study = getstudy(studyid)

    if form.validate_on_submit():
        lecture = {
            "moduleid": moduleid,
            "id": lectureid,
            "title": form.title.data,
            "short": form.short.data,
            "description": form.description.data,
            "semester": form.semester.data,
            "responsible": form.responsible.data,
        }

        print(lecture)

        # add api put request here

        return redirect(url_for('study_admin', studyid=studyid))

    return render_template("editLecture.html", form=form, title="Lehrveranstaltung bearbeiten", study=study.json(), moduleid=moduleid)
