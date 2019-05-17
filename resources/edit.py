from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from models.person import PersonModel
from models.telephone import TelephoneModel
from models.psychologist import PsychologistModel
from models.hospital import HospitalModel
from models.psychologist_hospital import PsychologistHospitalModel

from datetime import datetime


class EditPsychologist(Resource):
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
                        type=lambda d: datetime.strptime(d, '%d-%m-%Y')
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

    @jwt_required
    def put(self, crp):
        data = EditPsychologist.parser.parse_args()

        psychologist = PsychologistModel.find_by_crp(crp)

        if psychologist:
            if data['name']:
                psychologist.person_psy.name = data['name']
            if data['email']:
                psychologist.person_psy.email = data['email']
            if data['number']:
                psychologist.person_psy.telephones[0].number = data['number']
            if data['telephone_type']:
                psychologist.person_psy.telephones[0].telephone_type = data['telephone_type']
            if data['date_of_birth']:
                psychologist.date_of_birth = data['date_of_birth']
            if data['password']:
                psychologist.password = data['password']
            if data['registry_number']:
                psychologist.hospital_psychologists[0].hospital.registry_number = data['registry_number']
            if data['social_reason']:
                psychologist.hospital_psychologists[0].hospital.social_reason = data['social_reason']
            if data['crp']:
                return {'message': 'You cannot change the crp'}

        else:
            return {'message': 'User not found.'}, 404

        psychologist.save_to_db()

        return {'message': 'User updated'}, 200