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
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    telephone = db.relationship('Telephone', backref='owner1')
    natural_person = db.relationship('NaturalPerson', backref='owner2')
    legal_person = db.relationship('LegalPerson', backref='owner3')


class Telephone(db.Model):
    number = db.Column(db.String(11), primary_key=True, autoincrement=False)
    owner1_id = db.Column(db.Integer, db.ForeignKey('person.id'))


class NaturalPerson(db.Model):
    cpf = db.Column(db.String(11), primary_key=True, autoincrement=False)
    owner2_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    psychologist = db.relationship('Psychologist', backref='owner4')


class Psychologist(db.Model):
    crp = db.Column(db.String(128), primary_key=True, autoincrement=False)
    password = db.Column(db.String(128))
    owner4_id = db.Column(db.Integer, db.ForeignKey('natural_person.cpf'))


class LegalPerson(db.Model):
    cnpj = db.Column(db.String(128), primary_key=True, autoincrement=False)
    owner3_id = db.Column(db.Integer, db.ForeignKey('person.id'))


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_person = Person(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'])
    db.session.add(new_person)
    db.session.commit()

    new_telephone = Telephone(number=data['number'], owner1=new_person)
    db.session.add(new_telephone)
    db.session.commit()

    new_natural_person = NaturalPerson(cpf=data['cpf'], owner2=new_person)
    db.session.add(new_natural_person)
    db.session.commit()

    new_psychologist = Psychologist(crp=data['crp'], password=hashed_password, owner4=new_natural_person)
    db.session.add(new_psychologist)
    db.session.commit()

    return jsonify({'message': 'New user created'})


if __name__ == '__main__':
    app.run(debug=True)


# {"name": "Daniel", "password" : "12345", "email": "daniel_sousa.unb@hotmail.com", "number": "61123456789", "crp": "01/123445", "cpf": "12345678912"}