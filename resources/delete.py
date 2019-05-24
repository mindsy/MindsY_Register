from flask_restful import Resource
from models.psychologist import PsychologistModel


class DeleteUser(Resource):
    @classmethod
    def delete(cls, crp):
        psychologist = PsychologistModel.find_by_crp(crp)
        if psychologist:
            psychologist.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404
