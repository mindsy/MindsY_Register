# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from models.person import PersonModel
from models.telephone import TelephoneModel
from models.psychologist import PsychologistModel
from models.hospital import HospitalModel
from models.psychologist_hospital import PsychologistHospitalModel

class Register(Resource):

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
                        type=int,
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
                        type=str,
                        required=True,
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
        
    def post(self):
        data = Register.parser.parse_args()

        if PersonModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400
        
        if PsychologistModel.find_by_crp(data['crp']):
            return {"message": "A user with that crp already exists"}, 400

        if TelephoneModel.find_by_number(data['number']):
            return {"message": "A user with that number already exists"}, 400
        
        new_person = PersonModel(data['name'], data['email'])
        new_person.save_to_db()

        new_telephone = TelephoneModel(data['number'], data['telephone_type'], new_person)
        new_telephone.save_to_db()

        new_psychologist = PsychologistModel(data['crp'], data['password'],data['date_of_birth'], new_person)
        new_psychologist.save_to_db()

        if not HospitalModel.find_by_registry_number("4002"):
            new_hospital_person = PersonModel("Hospital da Crianca", "hospitalCrianca@gmail.com")
            new_hospital = HospitalModel("4002", "HOSPITAL DA CRIANA LTDA", new_hospital_person)
            new_psychologist_hospital = PsychologistHospitalModel(new_hospital, new_psychologist)

            new_psychologist_hospital.save_to_db()
            new_hospital_person.save_to_db()
            new_hospital.save_to_db()

        else:
            
            new_psychologist_hospital = PsychologistHospitalModel(HospitalModel.find_by_registry_number("4002"), new_psychologist)
            new_psychologist_hospital.save_to_db()

        return {"message": "User created successfully."}, 201

# {"name": "tactel", 
# "email": "tactelzeras@gmail.com",
# "number": "111111",
# "telephone_type": "residencial",
# "password": "mudeiasenha",
# "date_of_birth": "12/09/1999",
# "crp": "123456"
# }