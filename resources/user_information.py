from flask_restful import Resource
from models.psychologist import PsychologistModel


class ShowPsychologistInformationCRP(Resource):
    @staticmethod
    def get(crp):
        psychologists = PsychologistModel.find_by_crp(crp)
        if psychologists:
            person_info = psychologists.PERSON.json()
            psychologists_info = psychologists.json()
            hospital_info = psychologists.hospital_psychologists[0].HOSPITAL.json()
            psy_hosp_info = psychologists.hospital_psychologists[0].id_psycho_hosp

            output = {'Basic Informations': [person_info],
                      'Psychologist Information': [psychologists_info],
                      'Hospital': [hospital_info],
                      'id_psycho_hosp': psy_hosp_info}

            return {'User Information': output}
        return {'message': 'User not found.'}, 404
