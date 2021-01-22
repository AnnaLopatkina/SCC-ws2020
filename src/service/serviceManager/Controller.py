import json
import secrets

from flask import jsonify, request, abort
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from serviceManager import app, db, token_password, token_username
from serviceManager.Token import Token
from serviceManager.models import Study, Module, Lecture, StudiesModules, ModulesLectures

auth1 = HTTPBasicAuth()
auth2 = HTTPTokenAuth(scheme='Bearer')


@auth1.verify_password
def verify_password(username, password):
    if password == token_password and username == token_username:
        return username


@auth2.verify_token
def verify_token(token):
    for token1 in Token.query.all():
        if token == token1.token:
            return token


@app.route('/api/getToken', methods=['GET'])
@auth1.login_required()
def get_token():
    token = Token()
    token.token = secrets.token_urlsafe(5)
    db.session.add(token)
    db.session.commit()
    return jsonify({'token': token.token})


@app.route('/api/studies', methods=['GET'])
def get_studies():
    studies = Study.query.all()

    study_list = []

    for study in studies:
        study = {
            "id": study.study_id,
            "title": study.title,
            "description": study.description,
            "semesters": study.semesters,
            "degree": study.degree
        }
        study_list.append(study)
    return jsonify({'studies': study_list})


@app.route('/api/study/<int:study_id>', methods=['GET'])
def get_study(study_id):
    study = Study.query.filter_by(study_id=study_id).first()

    if not study:
        return jsonify({'message': 'No such study'})

    modules = get_modules(
        study_id)  # Get all Modules of ModulesOfStudies that belongs to this study ->and then get all lectures that
    # belong to these modules

    study_data = {'id': study.study_id, 'title': study.title, 'description': study.description,
                  'semesters': study.semesters, 'degree': study.degree, 'modules': modules}
    return jsonify({'study': study_data})


def get_modules(requested_study_id):
    modules = []

    data1 = db.session.query(Study, Module) \
        .filter(Study.study_id == requested_study_id) \
        .filter(Study.study_id == StudiesModules.study_id) \
        .filter(StudiesModules.module_id == Module.module_id) \
        .order_by(Study.study_id).all()

    for study, module in data1:

        data2 = db.session.query(Module, Lecture) \
            .filter(Module.module_id == module.module_id) \
            .filter(Module.module_id == ModulesLectures.module_id) \
            .filter(ModulesLectures.lecture_id == Lecture.lecture_id).all()

        lectures = []
        for module2, lecture in data2:

            lecture_new = {
                "id": lecture.lecture_id,
                "title": lecture.title,
                "short": lecture.short,
                "description": lecture.description,
                "semester": lecture.semester,
                "responsible": lecture.responsible
            }
            lectures.append(lecture_new)

        module_new = {
            "id": module.module_id,
            "title": module.title,
            "short": module.short,
            "duration": module.duration,
            "credits": module.credits,
            "description": module.description,
            "responsible": module.responsible,
            "teaching": module.teaching,
            "lectures": lectures
        }

        modules.append(module_new)

    return modules


@app.route('/api/study',
           methods=['PUT'])  # Updated vorhandenen Studiengang oder erzeugt neuen, je nachdem, ob id mit angeben ist;
@auth2.login_required()
def update_study():
    if not request.json:
        abort(400)

    if request.json["id"] == "":
        study = Study(request.json["title"], request.json["description"], request.json["semesters"],
                      request.json["degree"])
    else:
        study = Study.query.filter_by(study_id=request.json["id"]).first()
        study.title = request.json["title"]
        study.description = request.json["description"]
        study.semester = request.json["semesters"]
        study.degree = request.json[
            "degree"]  # wird momentan vom Client gar nicht zur Verfuegung gestellt, Aendern! -> mindestens in Forms, wahrscheinlich noch woanders
    db.session.add(study)
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/api/study/<int:study_id>/module',
           methods=['PUT'])  # Was machen wir mit den Attributen, die vielleicht nicht gegeben sind?
@auth2.login_required()
def update_module(study_id):
    if not request.json:
        abort(400)

    if request.json["id"] == "":
        module = Module(request.json["title"], request.json["short"], request.json["duration"], request.json["credits"],
                        request.json["description"], request.json["responsible"], request.json["teaching"])
    else:
        module = Module.query.filter_by(module_id=request.json["id"]).first()
        module.title = request.json["title"]
        module.short = request.json["short"]
        module.duration = request.json["duration"]
        module.credits = request.json["credits"]
        module.description = request.json["description"]
        module.responsible = request.json["responsible"]
        module.teaching = request.json["teaching"]

    db.session.add(module)  # Was ist die session? Kann man das so schreiben?
    db.session.commit()

    study = Study.query.filter_by(study_id=study_id).first()
    study.add_module(module)
    db.session.add(study)
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/api/study/<int:study_id>/module/<int:module_id>/lecture', methods=['PUT'])
@auth2.login_required()
def update_lecture(study_id, module_id):  # Zuweisung zum Modul fehlt noch
    if not request.json:
        abort(400)

    if request.json["id"] == "":
        lecture = Lecture(request.json["title"], request.json["short"], request.json["description"],
                          request.json["semester"], request.json["responsible"])
    else:
        lecture = Lecture.query.filter_by(lecture_id=request.json["id"]).first()
        lecture.title = request.json["title"]
        lecture.short = request.json["short"]
        lecture.description = request.json["description"]
        lecture.semester = request.json["semester"]
        lecture.responsible = request.json["responsible"]
    db.session.add(lecture)
    db.session.commit()

    module = Module.query.filter_by(module_id=module_id).first()
    module.add_lecture(lecture)
    db.session.add(module)
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
