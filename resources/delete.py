from flask_restful import Resource
from flask_jwt_extended import fresh_jwt_required
from models.person import PersonModel


class DeleteUser(Resource):
    @classmethod
    @fresh_jwt_required
    def delete(cls, id):
        person = PersonModel.find_by_id(id)
        if person:
            person.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404
