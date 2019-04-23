from flask_restful import Resource, reqparse, request
from models.person import PersonModel
from models.telephone import TelephoneModel
from models.psychologist import PsychologistModel
from models.hospital import HospitalModel
from models.psychologist_hospital import PsychologistHospitalModel

class DeleteUser(Resource):
    def delete(self, id):
        person = PersonModel.find_by_id(id)
        if person:
            person.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404