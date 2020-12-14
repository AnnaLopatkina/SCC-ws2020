from serviceManager import app, db


class Token(db.Model):
    token = db.Column(db.String(100), primary_key=True)
