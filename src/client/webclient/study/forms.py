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


class ModuleForm(FlaskForm):
    moduleid = HiddenField()
    title = StringField('Modulname', validators=[DataRequired()])
    short = StringField('Modulkürzel', validators=[DataRequired()])
    description = TextAreaField('Modulbeschreibung')
    duration = StringField('Dauer des Moduls')
    credits = StringField('Leistungspunkte')
    responsible = StringField('Verantwortlicher Dozent')
    teaching = StringField('Lehrform: x/x/x SWS')
    save = SubmitField('Modul erstellen')


class LectureForm(FlaskForm):
    lectureid = HiddenField()
    title = StringField('Name der Lehrveranstaltung', validators=[DataRequired()])
    short = StringField('Kürzel', validators=[DataRequired()])
    description = TextAreaField('Beschreibung')
    semester = IntegerField('Semester')
    responsible = StringField('Verantwortlich')
    save = SubmitField('Lehrveranstaltung erstellen')
