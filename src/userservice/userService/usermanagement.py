from werkzeug.routing import ValidationError

from userService.models import User, Role, Token


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
