from db import db


class HospitalModel(db.Model):
    __tablename__ = 'hospital'

    registry_number = db.Column(db.String, primary_key=True, autoincrement=False)
    social_reason = db.Column(db.String)

    hospital_person_id = db.Column(db.Integer, db.ForeignKey('person.id'), unique=True)
    hospital_psychologists = db.relationship('PsychologistHospitalModel', backref='hospital', lazy='dynamic', uselist=True)

    def __init__(self, registry_number, social_reason, hospital_person):
        self.registry_number = registry_number
        self.social_reason = social_reason
        self.hospital_person = hospital_person

    def json(self):
         return {'registry_number': self.registry_number, 'social_reason': self.social_reason}

    @classmethod
    def find_by_name(cls, registry_number):
        return cls.query.filter_by(registry_number=registry_number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()