# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt,
    get_jwt_identity
)
from security import encrypt_password
from datetime import datetime
from models.person import PersonModel
from models.telephone import TelephoneModel
from models.psychologist import PsychologistModel
from models.hospital import HospitalModel
from models.psychologist_hospital import PsychologistHospitalModel
from models.patient import PatientModel
from models.pat_psycho_hosp import Pat_Psycho_HospModel
from models.accountable import AccountableModel

class RegisterPsychologist(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('number',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('telephone_type',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('crp',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
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

    def post(self):
        data = RegisterPsychologist.parser.parse_args()

        if PersonModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        if PsychologistModel.find_by_crp(data['crp']):
            return {"message": "A user with that crp already exists"}, 400

        if TelephoneModel.find_by_number(data['number']):
            return {"message": "A user with that number already exists"}, 400

        new_person = PersonModel(data['name'], data['email'])
        new_person.save_to_db()

        new_telephone = TelephoneModel(data['number'], data['telephone_type'], new_person.id)
        new_telephone.save_to_db()
        
        password_crip = encrypt_password(data['password'])

        new_psychologist = PsychologistModel(data['crp'], password_crip, data['date_of_birth'], new_person.id)
        new_psychologist.save_to_db()

        if not HospitalModel.find_by_registry_number("4002"):
            new_hospital_person = PersonModel("Hospital da Crianca", "hospitalCrianca@gmail.com")
            new_hospital_person.save_to_db()

            new_hospital = HospitalModel("4002", "HOSPITAL DA CRIANCA LTDA", new_hospital_person.id)
            new_hospital.save_to_db()

            new_psychologist_hospital = PsychologistHospitalModel(new_hospital.registry_number, new_psychologist.crp)
            new_psychologist_hospital.save_to_db()

        else:
            hosp = HospitalModel.find_by_registry_number("4002")
            new_psychologist_hospital = PsychologistHospitalModel(hosp.registry_number, new_psychologist.crp)
            new_psychologist_hospital.save_to_db()

        return {"message": "User created successfully."}, 201
