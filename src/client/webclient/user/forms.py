from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, \
    HiddenField, validators
from wtforms.validators import ValidationError, Email, EqualTo, DataRequired

from webclient.user.models import User, Role


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('EMail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password',
                                                                                          message="Passwörter müssen gleich sein!")])
    terms = BooleanField('terms')
    register = SubmitField('register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Verwendung dieser EMail ist nicht möglich!')

    def validate_password(self, password):
        if password == "":
            raise ValidationError("Passwort darf nicht leer sein!")


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    login = SubmitField('login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("E-Mail oder Passwort ist falsch!")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError("E-Mail oder Passwort ist falsch!")
        elif not user.check_password(password.data):
            raise ValidationError("E-Mail oder Passwort ist falsch!")


class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    roles = SelectField('Rollen', choices=[], validate_choice=False)
    studies = SelectField('Studiengang', choices=[], validate_choice=False)
    semester = IntegerField('Semester',
                            validators=[validators.NumberRange(min=1, max=30, message="Semester unrealistisch")],
                            default=1)
    passwordold = PasswordField('Altes Passwort', validators=[])
    password = PasswordField('Neues Passwort', validators=[])
    password2 = PasswordField('Neues Passwort Wiederholen',
                              validators=[validators.EqualTo('password', message='Passwörter nicht gleich')])
    editprofile = SubmitField('Profil speichern')

    def validate_passwordold(self, passwordold):
        if passwordold.data != "":
            user = User.query.filter_by(email=self.email.data).first()
            if not user.check_password(passwordold.data):
                raise ValidationError('Passwort falsch')

    def validate_password(self, password):
        if self.passwordold.data != "" and password.data == "":
            raise ValidationError('Neues Passwort darf nicht leer sein!')


class RoleForm(FlaskForm):
    roleid = HiddenField()
    name = StringField('Rolle im System', validators=[DataRequired()])
    save = SubmitField('Rolle speichern')

    def validate_name(self, name):
        if name == "":
            raise ValidationError('Rollenname darf nicht leer sein!')
        else:
            for role in Role.query.all():
                if role.name == name:
                    raise ValidationError('Eine Rolle {} existiert bereits!'.format(name))


class APITokenForm(FlaskForm):
    username = StringField('Nutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])

    submit = SubmitField('Token anfordern')
