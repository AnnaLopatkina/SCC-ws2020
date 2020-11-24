from serviceManager import app, Study
from flask import jsonify


@app.route('/api/studies', methods=['GET'])
def get_studies():
    studies = Study.query.all()
    return jsonify({'studies': studies})


@app.route('/api/study/<study_id>', methods=['GET'])
def get_study(study_id):
    study = Study.query.filter_by(study_id=study_id).first()

    if not study:
        return jsonify({'massage': 'No such study'})

    study_data = {'study_id': study.study_id, 'title': study.title, 'description': study.description,
                  'semester': study.semester, 'degree': study.degree}
    return jsonify({'message': study_data})


@app.route('api/courses', methods=['GET'])
def get_courses():
    return ''


@app.route('api/course/<course_id>}', methods=['GET'])
def get_course(course_id):
    return ''


@app.route('api/courses/possible_courses/<user_id>', methods=['GET'])
def get_courses_for_user(user_id):
    return ''


@app.route('api/course/<course_id>', methods=['PUT'])
def update_course(course_id):
    return ''


@app.route('api/course/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    return ''


@app.route('api/course', methods=['POST'])
def create_course():
    return ''

