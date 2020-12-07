from serviceManager import db

class ModulesOfStudies(db.Model): #brauche ich noch einen Primaerschluessel?
    relation_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    study_id =db.Column(db.Integer)
