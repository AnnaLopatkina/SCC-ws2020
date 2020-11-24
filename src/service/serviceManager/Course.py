from serviceManager import db


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    responsible = db.Column(db.String(99))
    times = db.Column(db.String(99), nullable=False)

    def __init__(self, title, description, responsible, times):
        self.title = title
        self.description = description
        self.responsible = responsible
        self.times = times
