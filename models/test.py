from db import db
import enum


class TypeEnum(enum.Enum):
    verbal = "verbal"
    executivo = "executivo"


class TestModel(db.Model):
    __tablename__ = 'TEST'

    id_test = db.Column('id_test', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    description = db.Column('description', db.String(255))
    maximum_score = db.Column('maximum_score', db.Numeric(5))
    type_of_test = db.Column('type', db.Enum(TypeEnum), nullable=False)

    evaluation_tests = db.relationship('EvaluationTestModel', backref='TEST', lazy='dynamic',
                                       cascade='all, delete-orphan')

    def __init__(self, name, description, maximum_score, type_of_test):
        self.name = name
        self.description = description
        self.maximum_score = maximum_score
        self.type_of_test = type_of_test

    def json(self):
        return {
                    'id_test': self.id_test,
                    'name': self.name,
                    'description': self.description,
                    'maximum_score': str(self.maximum_score),
                    'type': self.type_of_test.value
                }

    @classmethod
    def find_by_id(cls, id_test):
        return cls.query.filter_by(id_test=id_test).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
