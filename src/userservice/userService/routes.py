import secrets

from flask import request, abort, jsonify
from flask_httpauth import HTTPTokenAuth

from userService import app, db
from userService.models import User, Token, Role
from userService.usermanagement import validate_email, get_role, get_user

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    for token1 in Token.query.all():
        if token == token1.key:
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
        return jsonify(response), 500

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
        return jsonify(response), 500

    if not user.check_password(password=request.json['password']):
        response = {
            'errors': [
                {
                    'error': 'login',
                }
            ]
        }
        return jsonify(response), 500

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

    return {'token': token.key, 'is_admin': user.is_admin(), 'id': user.id}, 200


@app.route('/api/user/<int:user_id>', methods=['GET'])
@auth.login_required()
def get_user_id(user_id):
    user = get_user(user_id)
    if user is None:
        response = generate_error(['user'])
        return response, 500

    roles = []
    for role in user.get_roles():
        roles.append({'name': role.name, 'id': role.id})

    response = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'study': user.study,
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
            return response, 500

    user.username = request.json['username']
    user.semester = request.json['semester']



    db.session.add(user)
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
