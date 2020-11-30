from serviceManager import db


class Study(db.Model):
    study_id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    semesters = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(99), nullable=False)

    def __init__(self, title, description, semesters, degree):
        self.title = title
        self.description = description
        self.semesters = semesters
        self.degree = degree
