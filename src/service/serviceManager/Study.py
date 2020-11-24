from serviceManager import db


class Study(db.Model):
    study_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(99), nullable=False)

    def __init__(self, title, description, semester, degree):
        self.title = title
        self.description = description
        self.semester = semester
        self.degree = degree
