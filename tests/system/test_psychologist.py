from datetime import datetime

from static.imports import *
from tests.base_test import BaseTest
import json


class PsychologistTest(BaseTest):

    def test_delete_psychologist(self):
        with self.app() as c:
            with self.app_context():
                date_text = "22-09-2018"
                date = datetime.strptime(date_text, '%d-%m-%Y').date()
                person = PersonModel('test', 'test@test.com').save_to_db()
                PsychologistModel('0000000', 'Test123', date, 1).save_to_db()
                r = c.delete('/psychologist/0000000')

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual({'message': 'User deleted.'}, json.loads(r.data))

    def test_create_psychologist(self):
        with self.app() as c:
            with self.app_context():
                r = c.post('/psychologist',
                           data={'name': 'test', 'email': 'teste@test.com', 'number': '0000000000',
                                 'telephone_type': 'pessoal', 'crp': '0000000', 'password': 'Test123',
                                 'date_of_birth': '18-04-1999', 'registry_number': '00000000000',
                                 'social_reason': 'TEST LTDA'})

                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(PsychologistModel.find_by_crp('0000000'))
                self.assertDictEqual({"message": "User created successfully."},
                                     json.loads(r.data))

    def test_create_duplicate_psychologist(self):
        with self.app() as c:
            with self.app_context():
                c.post('/psychologist',
                       data={'name': 'test', 'email': 'teste@test.com', 'number': '0000000000',
                             'telephone_type': 'pessoal', 'crp': '0000000', 'password': 'Test123',
                             'date_of_birth': '18-04-1999', 'registry_number': '00000000000',
                             'social_reason': 'TEST LTDA'})
                r = c.post('/psychologist',
                           data={'name': 'test', 'email': 'teste@test.com', 'number': '0000000000',
                                 'telephone_type': 'pessoal', 'crp': '0000000', 'password': 'Test123',
                                 'date_of_birth': '18-04-1999', 'registry_number': '00000000000',
                                 'social_reason': 'TEST LTDA'})

                self.assertEqual(r.status_code, 400)
