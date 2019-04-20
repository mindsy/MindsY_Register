from db import db


class PsychologistModel(db.Model):
    __tablename__ = 'psychologist'

    crp = db.Column(db.String, primary_key=True, autoincrement=False)
    password = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    
    person_psy_id = db.Column(db.Integer, db.ForeignKey('person.id'), unique=True)
    hospital_psychologists = db.relationship('PsychologistHospitalModel', backref='crp_psychologist', lazy='dynamic')

    def __init__(self, crp, password, date_of_birth, person_psy):
        self.crp = crp
        self.password = password
        self.person_psy = person_psy
        self.date_of_birth = date_of_birth

    def json(self):
        return {'crp': self.crp, 'date_of_birth':self.date_of_birth}

    @classmethod
    def find_by_name(cls, crp):
        return cls.query.filter_by(crp=crp).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()