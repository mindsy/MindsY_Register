from flask_restful import Resource, reqparse, request
from flask_jwt_extended import fresh_jwt_required
from models.person import PersonModel
from models.telephone import TelephoneModel
from models.psychologist import PsychologistModel
from models.hospital import HospitalModel
from models.psychologist_hospital import PsychologistHospitalModel


class DeleteUser(Resource):
    @fresh_jwt_required
    def delete(self, id):
        person = PersonModel.find_by_id(id)
        if person:
            person.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404