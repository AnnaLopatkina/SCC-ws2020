from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import ValidationError, Email, EqualTo, DataRequired, NumberRange
from clientManager.entities import User


class RegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])
    terms = BooleanField('terms')
    register = SubmitField('register')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    login = SubmitField('login')


class ProfileForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    studies = SelectField('studies', choices=[], validate_choice=False)
    editprofile = SubmitField('editprofile')


class StudyForm(FlaskForm):
    studyid = HiddenField()
    title = StringField('title', validators=[DataRequired()])
    semesters = IntegerField('semesters', validators=[DataRequired(), NumberRange(min=1, max=20, message="enter valid number of semesters")], default=6)
    description = TextAreaField('description')
    save = SubmitField('save')