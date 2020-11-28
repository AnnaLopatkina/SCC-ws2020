from webclient import db


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    semesters = db.Column(db.Integer(), primary_key=False)
