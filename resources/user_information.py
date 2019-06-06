from flask_restful import Resource
from models.psychologist import PsychologistModel


class ShowPsychologistInformationCRP(Resource):
    @staticmethod
    def get(crp):
        psychologists = PsychologistModel.find_by_crp(crp)
        if psychologists:
            person_info = psychologists.PERSON.json()
            psychologists_info = psychologists.json()

            obj_ph = psychologists.hospital_psychologists.all()
            hospital_info = None
            for ph in obj_ph:
                hospital_info = ph.HOSPITAL.json()

            psychologists_info.update({'person': person_info}),
            psychologists_info.update({'hospital': hospital_info})
            return psychologists_info
        return {'message': 'User not found.'}, 404
