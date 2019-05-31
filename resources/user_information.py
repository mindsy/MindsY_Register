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

            output = []
            psychologists_info.update({'person': person_info}),
            psychologists_info.update({'hospital': hospital_info})
            output.append(psychologists_info)

            return {"psychologist": output}
        return {'message': 'User not found.'}, 404
