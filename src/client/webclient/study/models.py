from webclient import db


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    semesters = db.Column(db.Integer(), primary_key=False)


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, primary_key=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    study_id = db.Column(db.Integer(), db.ForeignKey('study.id', ondelete='CASCADE'))

    def __init__(self, grade):
        self.grade = grade
