from serviceManager import db

class ModulesOfStudies(db.ModulesOfStudies): #brauche ich noch einen Primaerschluessel?
    module_id = db.Column(db.Integer)
    study_id =db.Column(db.Integer)
