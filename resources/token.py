from flask_restful import Resource
from models.psychologist import PsychologistModel


class TokenInformation(Resource):
    @staticmethod
    def get(crp):
        psychologists = PsychologistModel.find_by_crp(crp)
        if psychologists:

            output = {'crp': psychologists.crp,
                      'token': psychologists.token}

            return output
        return {'message': 'User not found.'}, 404