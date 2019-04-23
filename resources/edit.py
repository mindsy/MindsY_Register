from flask_restful import Resource, reqparse, request
from models.person import PersonModel
from models.telephone import TelephoneModel
from models.psychologist import PsychologistModel
from models.hospital import HospitalModel
from models.psychologist_hospital import PsychologistHospitalModel

class Edit(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('number',
                        type=int,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('telephone_type',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )

    parser.add_argument('password',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('date_of_birth',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )

    parser.add_argument('registry_number',
                        type=str,
                        required=False
                        )
    parser.add_argument('social_reason',
                        type=str,
                        required=False
                        )
    parser.add_argument('crp',
                        type=str,
                        required=False
                        )
    def put(self, id):
        data = Edit.parser.parse_args()

        person = PersonModel.find_by_id(id)

        if person:
            if data['name']:
                person.name = data['name']
            if data['email']:
                person.email = data['email']
            if data['number']:
                person.telephones[0].number = data['number']
            if data['telephone_type']:
                person.telephones[0].telephone_type = data['telephone_type']
            if data['date_of_birth']:
                person.psychologists.date_of_birth = data['date_of_birth']
            if data['password']:
                person.psychologists.password = data['password']
            if data['registry_number']:
                person.hospitals.registry_number = data['registry_number']
            if data['social_reason']:
                person.hospitals.social_reason = data['social_reason']
            if data['crp']:
                return {'message': 'You cannot change the crp'}

        else:
            return {'message': 'User not found.'}, 404

        person.save_to_db()

        return person.json()