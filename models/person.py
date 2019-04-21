from db import db

class PersonModel(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    telephones = db.relationship('TelephoneModel', backref='tel_person', lazy='dynamic')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def json(self):
        return {'name': self.name, 'telephones': [telephone.json() for telephone in self.telephones.all()]}

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()