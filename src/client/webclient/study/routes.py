import requests
from flask import render_template, redirect, url_for

from webclient import app
from webclient.config import *
from webclient.study.forms import StudyForm, ModuleForm, LectureForm
from webclient.study.studymanagement import getstudies, getstudy, update_module, update_lecture
from webclient.user.usermanagement import admin_required, check_login, getUser


@app.route("/studiesAdmin")
@admin_required
def studies_admin():
    r = getstudies()
    print(r.json()['studies'])
    return render_template("studies_admin.html", studies=r.json()['studies'])


@app.route("/editStudy/<int:studyid>", methods=['GET'])
@admin_required
def studies_edit_admin(studyid):
    if session['studyapi_token'] == '':
        return redirect(url_for("get_api_token"))

    r = getstudies()

    for a in r.json()['studies']:
        if a['id'] == studyid:
            print('found study')
            study = a

    form = StudyForm(studyid=studyid, title=study['title'], description=study['description'], degree=study['degree'])

    return render_template('study_admin_edit.html', form=form)


@app.route("/editStudy/<int:studyid>", methods=['POST'])
@admin_required
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
        headers_token["Authorization"] = "Bearer " + session['studyapi_token']

        r = requests.put(url=url, headers=headers_token, json=study)
        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

    return redirect(url_for('study_admin', studyid=studyid))


@app.route("/addStudy", methods=['GET'])
@admin_required
def studies_add_admin():
    if session['studyapi_token'] is None:
        return redirect(url_for("get_api_token"))

    form = StudyForm()
    return render_template('study_admin_edit.html', form=form)


@app.route("/addStudy", methods=['POST'])
@admin_required
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
        headers_token["Authorization"] = "Bearer " + session['studyapi_token']

        r = requests.put(url=url, headers=headers_token, json=study)

        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))

    return redirect(url_for('studies_admin'))


# @app.route("/myGrades", methods=['GET'])
# @check_login
# def mygrades():
#     data = db.session.query(Grade).filter(User.id == current_user.id)
#
#     if data is None:
#         return render_template("myGrades.html", error=True)
#
#     return render_template("myGrades.html", user=current_user)


@app.route("/myStudy", methods=['GET'])
@check_login
def mystudy():
    user = getUser(session['id'])

    if user.json()['study_id'] is None or '':
        return render_template("mystudy.html", error=True)

    r = getstudy(user.json()['study_id'])
    print(r.json())

    return render_template("mystudy.html", study=r.json(), user=user.json())


@app.route("/study/<int:studyid>/addModule", methods=['GET'])
@admin_required
def add_module(studyid):
    if session['studyapi_token'] is None:
        return redirect(url_for("get_api_token"))

    study = getstudy(studyid)
    form = ModuleForm()

    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>/addModule", methods=['POST'])
@admin_required
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

        update_module(studyid, module)

        return redirect(url_for('study_admin', studyid=studyid))

    study = getstudy(studyid)
    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>/editModule/<int:moduleid>", methods=['GET'])
@admin_required
def edit_module(studyid, moduleid):
    if session['studyapi_token'] is None:
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
@admin_required
def edit_module_post(studyid, moduleid):
    form = ModuleForm()
    study = getstudy(studyid)

    if form.validate_on_submit():
        module = {
            "id": moduleid,
            "title": form.title.data,
            "short": form.short.data,
            "description": form.description.data,
            "duration": form.duration.data,
            "credits": form.credits.data,
            "responsible": form.responsible.data,
            "teaching": form.teaching.data,
        }

        print(module)

        update_module(studyid, module)

        return redirect(url_for('studies_admin'))

    return render_template("editModule.html", form=form, title="Modul erstellen", study=study.json())


@app.route("/study/<int:studyid>")
@admin_required
def study_admin(studyid):
    study = getstudy(studyid)
    json = study.json()
    return render_template("study_admin.html", study=study.json())


# Lehrveranstaltungen verwalten

@app.route("/study/<int:studyid>/module/<int:moduleid>/addlecture", methods=['GET'])
@admin_required
def add_lecture(studyid, moduleid):
    if session['studyapi_token'] is None:
        return redirect(url_for("get_api_token"))

    study = getstudy(studyid)
    form = LectureForm()

    return render_template("editLecture.html", form=form, title="Modul erstellen", study=study.json(), moduleid=moduleid)


@app.route("/study/<int:studyid>/module/<int:moduleid>/addlecture", methods=['POST'])
@admin_required
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

        update_lecture(studyid, moduleid, lecture)

        return redirect(url_for('study_admin', studyid=studyid))

    return render_template("editLecture.html", form=form, title="Modul erstellen", study=study.json(), moduleid=moduleid)


@app.route("/study/<int:studyid>/module/<int:moduleid>/editLecture/<int:lectureid>", methods=['GET'])
@admin_required
def edit_lecture(studyid, moduleid, lectureid):
    if session['studyapi_token'] is None:
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
@admin_required
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

        update_lecture(studyid, moduleid, lecture)

        return redirect(url_for('study_admin', studyid=studyid))

    return render_template("editLecture.html", form=form, title="Lehrveranstaltung bearbeiten", study=study.json(), moduleid=moduleid)
