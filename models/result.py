from db import db


class ResultModel(db.Model):
    __tablename__ = 'RESULT'

    id_result = db.Column('id_result', db.Integer, primary_key=True)
    gross_score = db.Column('gross_score', db.Numeric(5), nullable=False)
    considerate_score = db.Column('considerate_score', db.Numeric(5), nullable=False)
    classification = db.Column('classification', db.String(20), nullable=False)

    evaluation_test_result_id_evaluation_test = db.Column('fk_evaluation_test',
                                                          db.Integer, db.ForeignKey('EVALUATION_TEST.id_evaluation_test'),
                                                          unique=True, nullable=False)

    def __init__(self, gross_score, considerate_score, classification, evaluation_test_result_id_evaluation_test):
        self.gross_score = gross_score
        self.considerate_score = considerate_score
        self.classification = classification
        self.evaluation_test_result_id_evaluation_test = evaluation_test_result_id_evaluation_test

    def json(self):
        return {
                    'id_result': self.id_result,
                    'gross_score': str(self.gross_score),
                    'considerate_score': str(self.considerate_score),
                    'classification': self.classification,
                }

    @classmethod
    def find_by_id(cls, id_result):
        return cls.query.filter_by(id_result=id_result).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
