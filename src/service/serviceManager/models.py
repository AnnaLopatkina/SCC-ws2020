from sqlalchemy import Table

from serviceManager import db


class ModulesLectures(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    lecture_id = db.Column(db.Integer(), db.ForeignKey('lecture.lecture_id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'))


class StudiesModules(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    study_id = db.Column(db.Integer(), db.ForeignKey('study.study_id'))
    module_id = db.Column(db.Integer(), db.ForeignKey('module.module_id'))


class Study(db.Model):
    __tablename__ = 'study'
    study_id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    semesters = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(99), nullable=False)
    modules = db.relationship('Module', secondary='studies_modules', backref=db.backref('studies', lazy='dynamic'))

    def __init__(self, title, description, semesters, degree):
        self.title = title
        self.description = description
        self.semesters = semesters
        self.degree = degree

    def add_module(self, module):
        self.modules.append(module)

    def remove_module(self, module):
        self.modules.remove(module)


class Module(db.Model):
    __tablename__ = 'module'
    module_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # muss doch gar nicht unique sein
    short = db.Column(db.String(200), nullable=False)  # muss doch gar nicht unique sein, hier String(200) wohl zu gross
    duration = db.Column(db.Integer(), nullable=False)  # Datentyp nochmal festlegen
    credits = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    responsible = db.Column(db.String(99))
    teaching = db.Column(db.String(99))

    lectures = db.relationship('Lecture', secondary='modules_lectures', backref=db.backref('modules', lazy='dynamic'))

    def __init__(self, title, short, duration, credits, description, responsible, teaching):
        self.title = title
        self.description = description
        self.responsible = responsible
        self.short = short
        self.duration = duration
        self.credits = credits
        self.teaching = teaching

    def add_lecture(self, lecture):
        self.lectures.append(lecture)


class Lecture(db.Model):
    __tablename__ = 'lecture'
    lecture_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    short = db.Column(db.String(99)) #String sollte noch kuerzer sein koennen
    semester = db.Column(db.Integer)
    responsible = db.Column(db.String(99))

    def __init__(self, title, short, description, semester, responsible):
        self.title = title
        self.description = description
        self.responsible = responsible
        self.semester = semester
        self.short = short
        #self.times = times
