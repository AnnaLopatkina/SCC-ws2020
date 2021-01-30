import secrets

from flask import request, abort, jsonify
from flask_httpauth import HTTPTokenAuth

from userService import app, db
from userService.models import User, Token, Role, Study
from userService.usermanagement import validate_email, get_role, get_user, find_users, is_admin_token, set_role

auth = HTTPTokenAuth(scheme='Bearer')
auth2 = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    for token1 in Token.query.all():
        if token == token1.key:
            return token


@auth2.verify_token
def verify_token(token):
    for token1 in Token.query.all():
        if token == token1.key and is_admin_token(token):
            return token


@app.route('/api/registerUser', methods=['PUT'])
def register_user():
    print(request.json)

    if not request.json:
        abort(400)

    if validate_email(request.json['email']) is False:
        response = {
            'errors': [
                {
                    'error': 'email',
                }
            ]
        }
        return jsonify(response), 400

    print("register new user")

    user = User(username=request.json['name'], email=request.json['email'])
    user.set_password(request.json['password'])
    user.set_role(get_role("STUDENT"))

    db.session.add(user)
    db.session.commit()

    response = {
        'success': 'True'
    }

    return response, 200


@app.route('/api/loginToken', methods=['POST'])
def login_token():
    if not request.json:
        abort(400)

    a = request.json

    mail = request.json['email']

    user = User.query.filter_by(email=request.json['email']).first()

    if user is None:
        response = {
            'errors': [
                {
                    'error': 'login',
                }
            ]
        }
        return jsonify(response), 400

    if not user.check_password(password=request.json['password']):
        response = {
            'errors': [
                {
                    'error': 'login',
                }
            ]
        }
        return jsonify(response), 400

    token = Token()
    if user.token is None:

        print("key does not exist")
        token.key = secrets.token_urlsafe(5)
        db.session.add(token)
        user.token = token.key
        db.session.add(user)
        db.session.commit()

    else:
        print("key exists")
        token.key = user.token

    user = User.query.filter_by(email=request.json['email']).first()

    return {'token': token.key, 'is_admin': user.is_admin(), 'id': user.id, 'study_token': user.stoken}, 200


@app.route('/api/user/<int:user_id>', methods=['GET'])
@auth.login_required()
def get_user_id(user_id):
    user = get_user(user_id)
    if user is None:
        response = generate_error(['user'])
        return response, 400

    roles = []
    roles_test = user.get_roles()

    for role in user.get_roles():
        roles.append({'name': role.name, 'id': role.id})

    if user.study is None:
        study_id = -1
        study_title = ''
    else:
        study_id = user.study
        study_title = Study.query.filter_by(id=user.study).first().title

    response = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'study_id': study_id,
        'study_title': study_title,
        'roles': roles,
        'semester': user.semester
    }
    return response, 200


@app.route('/api/getRoles', methods=['GET'])
@auth.login_required()
def get_roles():
    roles = Role.query.all()

    roles_resp = []

    for role in roles:
        roles_resp.append({'name': role.name, 'id': role.id})

    return {'roles': roles_resp}, 200


@app.route('/api/editUser', methods=['PUT'])
@auth.login_required()
def edit_user():
    print(request.headers.get('Authorization').replace('Bearer ', ''))
    print(is_admin_token(request.headers.get('Authorization').replace('Bearer ', '')))
    if not request.json:
        abort(400)

    user = User.query.filter_by(id=request.json['id']).first()

    if request.json['passwordold'] != '':
        print('new pw')
        if user.check_password(request.json['passwordold']):
            print("set new pw")
            user.set_password(request.json['passwordnew'])
        else:
            print("password wrong")
            response = generate_error(["password"])
            return response, 400

    user.username = request.json['username']
    user.semester = request.json['semester']

    if request.json['study']['id'] != '':

        if Study.query.filter_by(id=request.json['study']['id']).first() is not None:
            user.study = Study.query.filter_by(id=request.json['study']['id']).first().id
        else:
            new_study = Study()
            new_study.id = request.json['study']['id']
            new_study.title = request.json['study']['title']

            db.session.add(new_study)
            user.study = new_study.id
            db.session.add(user)
            db.session.commit()

    # edit roles only if admin is doing it
    if is_admin_token(request.headers.get('Authorization').replace('Bearer ', '')):
        set_role(user, request.json['role'])

    db.session.add(user)
    db.session.commit()

    return {'success': True}, 200


@app.route('/api/users', methods=['GET'])
@auth2.login_required()
def get_users():
    data = find_users()

    users = []

    for user, study in data:
        roles = []
        for role in user.get_roles():
            roles.append({'name': role.name, 'id': role.id})

        if study is None:
            study = Study()
            study.id = '-1'
            study.title = ''

        user = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'semester': user.semester,
            'roles': roles,
            'study_id': study.id,
            'study_title': study.title
        }

        users.append(user)

    return {'users': users}, 200


@app.route("/api/setStudyToken/<int:user_id>", methods=['PUT'])
@auth2.login_required()
def set_study_token(user_id):
    if not request.json:
        abort(400)

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return generate_error(["user"]), 400

    user.study_api_token = request.json['study_token']

    db.session.add(user)
    db.session.commit()

    return {'success': True}, 200


@app.route("/api/addRole", methods=['PUT'])
@auth2.login_required()
def add_role():
    if not request.json:
        abort(400)

    if Role.query.filter_by(name=request.json['name']).first() is not None:
        return generate_error(['role']), 400

    role = Role()
    role.name = request.json['name']

    db.session.add(role)
    db.session.commit()

    return {'success': True}, 200


def generate_error(errors):
    errorlist = []
    for error in errors:
        errorlist.append({'error': error})

    response = {
        'errors': errorlist
    }

    return response


