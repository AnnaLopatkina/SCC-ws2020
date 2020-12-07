from serviceManager import db

class LecturesOfAModule(db.Model): #brauche ich noch einen Primaerschluessel?
    relation_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    lecture_id =db.Column(db.Integer)
