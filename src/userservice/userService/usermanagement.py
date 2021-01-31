from werkzeug.routing import ValidationError

from userService import db
from userService.models import User, Role, Token, Study


def validate_email(email):
    user = User.query.filter_by(email=email).first()
    print("email does not exists {}".format(user is None))
    return user is None


def get_role(rolestring):
    role = Role.query.filter_by(name=rolestring).first()
    return role


def validate_token(token):
    token1 = Token.query.filter_by(key=token).first()
    return token1 is not None


def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


def find_users():
    return db.session.query(User, Study).outerjoin(Study).all()


def add_role(user, rolestring):
    role = Role.query.filter_by(name=rolestring).first()
    print(role)
    if role is None:
        print("create new Role {}".format(rolestring))
        role = Role()
        role.name = rolestring
        db.session.add(role)

    print("add role to user")
    user.roles.append(role)

    db.session.add(user)
    db.session.commit()


def set_role(user, role_id):
    role = Role.query.filter_by(id=role_id).first()
    print(role)

    print("add role to user")
    user.roles.clear()
    user.roles.append(role)

    db.session.add(user)
    db.session.commit()


def is_admin_token(token):
    for user in User.query.all():
        for role in user.get_roles():
            print(user.token)
            if role.name == "ADMIN" and user.token == token:
                return True
    return False
