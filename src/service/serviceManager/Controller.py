from serviceManager import app, db
from serviceManager.Study import Study
from serviceManager.Module import Module
from flask import jsonify, request, abort
from serviceManager.Lecture import Lecture
from ServiceManager.LecturesOfAModule import LecturesOfAModule
from ServiceManager.ModulesOfStudies import ModulesOfStudies


@app.route('/api/studies', methods=['GET'])
def get_studies():
    studies = Study.query.all()

    study_list = []

    for study in studies:
        study = {
            "id": study.study_id,
            "title": study.title,
            "description": study.description,
            "semesters": study.semesters
        }
        study_list.append(study)
    return jsonify({'studies': study_list})


@app.route('/api/study/<int:study_id>', methods=['GET'])
def get_study(study_id):
    study = Study.query.filter_by(study_id=study_id).first()

    if not study:
        return jsonify({'message':a 'No such study'})

    modules = get_modules(study_id) #Get all Modules of ModulesOfStudies that belongs to this study ->and then get all lectures that belong to these modules

    study_data = {'id': study.study_id, 'title': study.title, 'description': study.description,
                  'semesters': study.semesters, 'degree': study.degree, 'modules': modules}
    return jsonify({'study': study_data})

def get_modules(requested_study_id):
    module_list = []
    modulesOfAStudy = ModulesOfStudies.query.filter_by(study_id = requested_study_id)
    for moduleId in modulesOfAStudy:
        module = Module.query.filter_by(module_id=moduleId).first()
        lecture_list = []
        lecturesOfAModule = LecturesOfAModule.query.filter_by(module_id=moduleId)
        for lectureId in lecturesOfAModule:
            lecture = Lecture.query.filter_by(lecture_id = lectureId).first()
            lecture = {
                "id": lecture.lecture_id,
                "title": lecture.title,
                "short": lecture.short,
                "description": lecture.description,
                "semester": lecture.semester,
                "responsible": lecture.responsible
            }
            lecture_list.append(lecture)
        module = {
            "id": module.module_id,
            "title": module.title,
            "short": module.short,
            "duration": module.duration,
            "credits": module.credits,
            "description": module.description,
            "responsible": module.responsible,
            "teaching": module.teaching,
            "lectures": lecture_list
        }
        module_list.append(module)
        return module_list

@app.route('/api/study', methods=['PUT']) #Updated vorhandenen Studiengang oder erzeugt neuen, je nachdem, ob id mit angeben ist;
def update_study():
    if not request.json:
        abort(400)

    if request.json["id"] == "":
        study = Study(request.json["title"], request.json["description"], request.json["semesters"], request.json["degree"])
    else:
        study = Study.query.filter_by(study_id=request.json["id"]).first()
        study.title = request.json["title"]
        study.description = request.json["description"]
        study.semester = request.json["semesters"]
        study.degree = request.json["degree"] #wird momentan vom Client gar nicht zur Verfuegung gestellt, Aendern! -> mindestens in Forms, wahrscheinlich noch woanders
    db.session.add(study)
    db.session.commit()
    return 200 #wenn keine Fehler vorhanden sind, sonst returne 3xx error


@app.route('/api/study/<int:study_id>/module', methods=['PUT']) #Was machen wir mit den Attributen, die vielleicht nicht gegeben sind?
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
    db.session.add(module) #Was ist die session? Kann man das so schreiben?
    db.session.commit()
    return 200 #wenn keine Fehler vorhanden sind, sonst returne 3xx error


@app.route('/api/study/<int:study_id>/module/<int:module_id>/lecture', methods=['PUT'])
def update_lecture(): #Zuweisung zum Modul fehlt noch
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
    return 200 #wenn keine Fehler vorhanden sind, sonst returne 3xx error


#@app.route('/api/lectures', methods=['GET'])
#def get_courses():
#    return ''


#@app.route('/api/lecture/<lecture_id>}', methods=['GET'])
#def get_course(course_id):
#    return ''


#@app.route('/api/lecture/possible_lectures/<user_id>', methods=['GET'])
#def get_courses_for_user(user_id):
#    return ''


#@app.route('/api/lecture/<lecture_id>', methods=['DELETE'])
#def delete_lecture(lecture_id):
#    return ''



