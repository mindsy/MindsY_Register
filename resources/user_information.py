from flask_restful import Resource, reqparse, request
from models.person import PersonModel
from models.telephone import TelephoneModel
from models.psychologist import PsychologistModel
from models.hospital import HospitalModel
from models.psychologist_hospital import PsychologistHospitalModel

class ShowInformationUser(Resource):
    def get(self, id):
        person = PersonModel.find_by_id(id)
        if person:
            person_info = person.json()
            crp = person.psychologists.crp
            date_of_birth = person.psychologists.date_of_birth
            password = person.psychologists.password

            hospital = PersonModel.find_by_id(2)
            registry_number = hospital.hospitals.registry_number
            social_reason = hospital.hospitals.social_reason

            output = {'Basic Informations': [person_info], 'Psychologist Information': {'crp': crp, 'date of birth': date_of_birth, 'password': password},
            'Hospital': {'social_reason': social_reason, 'registry_number': registry_number}}

            return {'User Information': output}
        return {'message': 'Item not found.'}, 404