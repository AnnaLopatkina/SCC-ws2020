from serviceManager import app, db
from serviceManager.Study import Study
from flask import jsonify, request, abort


@app.route('/api/studies', methods=['GET'])
def get_studies():
    studies = Study.query.all()

    study_list = []

    for study in studies:
        study = {
            "id": study.study_id,
            "title": study.title,
            "description": study.description
        }
        study_list.append(study)
    return jsonify({'studies': study_list})


@app.route('/api/study/<int:study_id>', methods=['GET'])
def get_study(study_id):
    study = Study.query.filter_by(study_id=study_id).first()

    if not study:
        return jsonify({'massage': 'No such study'})

    study_data = {'study_id': study.study_id, 'title': study.title, 'description': study.description,
                  'semester': study.semester, 'degree': study.degree}
    return jsonify({'message': study_data})


@app.route('/api/study', methods=['PUT'])
def update_study():
    if not request.json:
        abort(400)

    if request.json["id"] == "":
        study = Study(request.json["title"], request.json["description"], 8, "degree")
    else:
        study = Study.query.filter_by(study_id=request.json["id"]).first()
        study.title = request.json["title"]
        study.description = request.json["description"]
        study.semester = 8
        study.degree = "degreeeeee"
    db.session.add(study)
    db.session.commit()


@app.route('/api/courses', methods=['GET'])
def get_courses():
    return ''


@app.route('/api/course/<course_id>}', methods=['GET'])
def get_course(course_id):
    return ''


@app.route('/api/courses/possible_courses/<user_id>', methods=['GET'])
def get_courses_for_user(user_id):
    return ''


@app.route('/api/course/<course_id>', methods=['PUT'])
def update_course(course_id):
    return ''


@app.route('/api/course/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    return ''


@app.route('/api/course', methods=['POST'])
def create_course():
    return ''

