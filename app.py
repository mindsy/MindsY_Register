from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mindsy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/daniel/Documents/MDS/mindsy-microservice-register/mindsy.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    telephone = db.relationship('telephone', backref='owner1')
    natural_person = db.relationship('natural_person', backref='owner2')
    legal_person = db.relationship('legal_person', backref='owner3')


class Telephone(db.Model):
    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    owner1_id = db.Column(db.Integer, db.ForeignKey('person.id'))


class NaturalPerson(db.Model):
    cpf = db.Column(db.Integer, primary_key=True, autoincrement=False)
    owner2_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    psychologist = db.relationship('psychologist', backref='owner4')


class Psychologist(db.Model):
    crp = db.Column(db.Integer, primary_key=True, autoincrement=False)
    owner4_id = db.Column(db.Integer, db.ForeignKey('natural_person.cpf'))


class LegalPerson(db.Model):
    cnpj = db.Column(db.Integer, primary_key=True, autoincrement=False)
    owner3_id = db.Column(db.Integer, db.ForeignKey('person.id'))

