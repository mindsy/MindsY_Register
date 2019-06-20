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

            output = {'person': person_info,
                      'psychologist': psychologists_info,
                      'hospital': hospital_info
                      }

            return output
        return {'message': 'User not found.'}, 404
    
