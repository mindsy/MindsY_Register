from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from models.psychologist import PsychologistModel
from models.person import PersonModel


class ShowInformationUserID(Resource):
    @jwt_required
    def get(self, crp):
        psychologists = PsychologistModel.find_by_crp(crp)
        if psychologists:
            person_info = psychologists.person_psy.json()
            psychologists_info = psychologists.json()
            hospital_info = psychologists.hospital_psychologists[0].hospital.json()
            psy_hosp_info = psychologists.hospital_psychologists[0].id_psycho_hosp

            output = {'Basic Informations': [person_info], 'Psychologist Information': [psychologists_info] , 'id_psychogist_hospital': psy_hosp_info,
            'Hospital': [hospital_info]}

            return {'User Information': output}
        return {'message': 'User not found.'}, 404