from serviceManager import db

class Module(db.Model):
    module_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False) #muss doch gar nicht unique sein
    short = db.Column(db.String(200), unique=True, nullable=False) #muss doch gar nicht unique sein, hier String(200) wohl zu gross
    duration = db.Column(db.Time(), nullable=False)  # Datentyp nochmal festlegen
    credits = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    responsible = db.Column(db.String(99))
    teaching = db.Column(db.String(99))

    def __init__(self, title, short, duration, credits, description, responsible, teaching):
        self.title = title
        self.description = description
        self.responsible = responsible
        self.short = short
        self.duration = duration
        self.credits = credits
        self.teaching = teaching
