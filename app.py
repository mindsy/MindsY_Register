from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mindsy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/daniel/Documents/MDS/mindsy-microservice-register/mindsy.db'

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    cpf = db.Column(db.String(11))
    telephone = db.relationship('Telephone', backref='tel_person', lazy='dynamic')
    hospital = db.relationship('Hospital', backref='hospital_person', uselist=False)
    psychologist = db.relationship('Psychologist', backref='person_psy', uselist=False)


class Telephone(db.Model):
    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    tel_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


class Hospital(db.Model):
    cnpj = db.Column(db.String, primary_key=True, autoincrement=False)
    social_reason = db.Column(db.String)
    hospital_person_id = db.Column(db.Integer, db.ForeignKey('person.id'), unique=True)
    hospital = db.relationship('HospitalPsychologist', backref='hospital', lazy='dynamic', uselist=True)


class Psychologist(db.Model):
    crp = db.Column(db.String, primary_key=True, autoincrement=False)
    password = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    person_psy_id = db.Column(db.Integer, db.ForeignKey('person.id'), unique=True)
    hospital_psychologist = db.relationship('HospitalPsychologist', backref='crp_psychologist',
                                            lazy='dynamic', uselist=True)


class HospitalPsychologist(db.Model):
    initial_date = db.Column(db.String)
    crp_psychologist_crp = db.Column(db.Integer, db.ForeignKey('psychologist.crp'), unique=False,
                                     primary_key=True, autoincrement=False)
    hospital_cnpj = db.Column(db.Integer, db.ForeignKey('hospital.cnpj'), unique=False,
                              primary_key=True, autoincrement=False)


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_person = Person(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], cpf=data['cpf'])
    db.session.add(new_person)
    db.session.commit()

    new_telephone = Telephone(number=data['number'], tel_person=new_person)
    db.session.add(new_telephone)
    db.session.commit()

    new_hospital = Hospital(cnpj=data['cnpj'], social_reason=data['social_reason'], hospital_person=new_person)
    db.session.add(new_hospital)
    db.session.commit()

    new_psychologist = Psychologist(crp=data['crp'], password=hashed_password, date_of_birth=data['date_of_birth'],
                                    person_psy=new_person)
    db.session.add(new_psychologist)
    db.session.commit()

    new_hospital_psychologist = HospitalPsychologist(initial_date=data['initial_date'],
                                                     crp_psychologist=new_psychologist, hospital=new_hospital)
    db.session.add(new_hospital_psychologist)
    db.session.commit()

    return jsonify({'message': 'New user created'})


if __name__ == '__main__':
    app.run(debug=True)

