from serviceManager import db

class LecturesOfAModule(db.LecturesOfAModule): #brauche ich noch einen Primaerschluessel? 
    module_id = db.Column(db.Integer)
    lecture_id =db.Column(db.Integer)
