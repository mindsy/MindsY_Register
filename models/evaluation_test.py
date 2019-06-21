from db import db


class EvaluationTestModel(db.Model):
    __tablename__ = 'EVALUATION_TEST'

    id_evaluation_test = db.Column('id_evaluation_test', db.Integer, primary_key=True)

    test_pat_psycho_hosp_id_evaluation = db.Column('fk_evaluation',
                                                   db.Integer, db.ForeignKey('EVALUATION.id_evaluation'))
    test_pat_psycho_hosp_id_test = db.Column('fk_test',
                                             db.Integer, db.ForeignKey('TEST.id_test'))

    results = db.relationship('ResultModel', backref='EVALUATION_TEST', uselist=False, cascade='all, delete-orphan')

    def __init__(self, test_pat_psycho_hosp_id_evaluation, test_pat_psycho_hosp_id_test):
        self.test_pat_psycho_hosp_id_evaluation = test_pat_psycho_hosp_id_evaluation
        self.test_pat_psycho_hosp_id_test = test_pat_psycho_hosp_id_test


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
