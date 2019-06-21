from db import db


class EvaluationModel(db.Model):
    __tablename__ = 'EVALUATION'

    id_evaluation = db.Column('id_evaluation', db.Integer, primary_key=True)
    dt_start = db.Column('dt_start', db.DateTime, nullable=False)
    dt_end = db.Column('dt_end', db.DateTime, nullable=False)
    conclusion = db.Column('conclusion', db.Text)
    anamnese = db.Column('anamnese', db.Text)

    test_pat_psycho_hosp_id_pat_psycho_hosp = db.Column('fk_pat_psycho_hosp',
                                                        db.Integer, db.ForeignKey('PAT_PSYCHO_HOSP.id_pat_psycho_hosp'))
    evaluation_tests = db.relationship('EvaluationTestModel', backref='EVALUATION', lazy='dynamic',
                                       cascade='all, delete-orphan')

    def __init__(self, dt_start, dt_end, conclusion, anamnese, test_pat_psycho_hosp_id_pat_psycho_hosp):
        self.dt_start = dt_start
        self.dt_end = dt_end
        self.conclusion = conclusion
        self.anamnese = anamnese
        self.test_pat_psycho_hosp_id_pat_psycho_hosp = test_pat_psycho_hosp_id_pat_psycho_hosp

    def json(self):
        return {
                    'id_evaluation': self.id_evaluation,
                    'dt_start': str(self.dt_start),
                    'dt_end': str(self.dt_end),
                    'conclusion': self.conclusion,
                    'anamnese': self.anamnese,
                }

    @classmethod
    def find_by_id(cls, id_evaluation):
        return cls.query.filter_by(id_evaluation=id_evaluation).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
