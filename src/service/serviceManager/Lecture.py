from serviceManager import db


class Lecture(db.Model):
    lecture_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    short = db.Column(db.String(99)) #String sollte noch kuerzer sein koennen
    semester = db.Column(db.Integer)
    responsible = db.Column(db.String(99))
    #times = db.Column(db.String(99), nullable=False) #wofuer brauchen wir times?

    def __init__(self, title, short, description, semester, responsible):
        self.title = title
        self.description = description
        self.responsible = responsible
        self.semester = semester
        self.short = short
        #self.times = times
