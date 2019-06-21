from flask_restful import Resource
from static.imports import *
from db import db

class DeleteUser(Resource):
    @classmethod
    def delete(cls, crp):
        psychologist = PsychologistModel.find_by_crp(crp)
        if not psychologist:
            return {'message': 'User not found.'}, 404

        if PsychologistModel.find_by_crp(crp):
            persons = (db.session.query(PersonModel)
            .filter(PsychologistModel.crp == crp)
            .filter(HospitalModel.registry_number == '4002')
            .filter(PsychologistModel.crp == PsychologistHospitalModel.crp_psychologist_crp)
            .filter(HospitalModel.registry_number == PsychologistHospitalModel.hospital_registry_number)
            .filter(PatientModel.id_patient == PatPsychoHospModel.patient_hosp_psy_id_patient)
            .filter(PsychologistHospitalModel.id_psycho_hosp == PatPsychoHospModel.pat_psycho_hosp_id_psycho_hosp)
            .filter(PersonModel.id == PatientModel.person_pat_id) 
            .all())

            for person in persons:
                id_patient = person.patients.id_patient
                if PatientModel.find_by_id(id_patient):
                    evaluations = (db.session.query(EvaluationModel)
                            .filter(HospitalModel.registry_number == '4002')
                            .filter(PsychologistModel.crp == crp)
                            .filter(PatientModel.id_patient == id_patient)
                            .filter(PsychologistHospitalModel.id_psycho_hosp ==
                                    PatPsychoHospModel.pat_psycho_hosp_id_psycho_hosp)
                            .filter(PatientModel.id_patient == PatPsychoHospModel.patient_hosp_psy_id_patient)
                            .filter(PatPsychoHospModel.id_pat_psycho_hosp ==
                                    EvaluationModel.test_pat_psycho_hosp_id_pat_psycho_hosp).all())
                    for evaluation in evaluations:
                        evaluation.delete_from_db()
                    person.delete_from_db()

            psychologist.PERSON.delete_from_db()
            psychologist.delete_from_db()

        return {'message': 'User deleted.'}
        