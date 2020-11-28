from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, \
    HiddenField
from wtforms.validators import DataRequired, NumberRange


class StudyForm(FlaskForm):
    studyid = HiddenField()
    title = StringField('Studiengang', validators=[DataRequired()])
    semesters = IntegerField('Anzahl Semester', validators=[DataRequired(), NumberRange(min=1, max=20,
                                                                                        message="enter valid number of semesters")],
                             default=6)
    description = TextAreaField('Beschreibung')
    save = SubmitField('save')
