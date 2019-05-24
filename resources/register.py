# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from security import encrypt_password
from datetime import datetime
from static.imports import *


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

    @staticmethod
    def post():
        data = RegisterPsychologist.parser.parse_args()

        if PersonModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        if PsychologistModel.find_by_crp(data['crp']):
            return {"message": "A user with that crp already exists"}, 400

        if TelephoneModel.find_by_number(data['number']):
            return {"message": "A user with that number already exists"}, 400

        if len(data['name']) <= 1:
            return {"message": "Type a valid name"}

        if len(data['crp']) != 7 or not data['crp'].isdigit():
            return {"message": "Type a valid crp"}

        if data['registry_number']:
            if len(data["registry_number"]) > 14:
                return {"message": "Type a valid registry_number"}

        if data['password']:
            if not any(char.isdigit() for char in data['password']):
                return {"message": "The password needs one digit, at least"}

            if len(data['password']) < 7:
                return {"message": "The password needs 7 characters, at least"}

            if data['password'].islower():
                return {"message": "The password needs one upper character, at least"}

            if data['password'].isupper():
                return {"message": "The password needs one lower character, at least"}

            if not data['password'].isalnum():
                return {"message": "The password does not support symbols, special characters and empty spaces"}

            if data['password'].isdigit():
                return {"message": "The password does not to be only numbers"}

            if data['password'].isspace():
                return {"message": "The password does not to be only blank characters"}

        if len(data['number']) > 15 or len(data['number']) < 8 or not data['number'].isdigit():
            return {"message": "Type a valid telephone_number"}

        if str(data['telephone_type'].lower()) != str("residencial") and str(data['telephone_type'].lower()) != str("pessoal") \
                and str(data['telephone_type'].lower()) != str("comercial"):
            return {"message": "Type a valid telephone_type"}

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
