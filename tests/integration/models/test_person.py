from static.imports import *
from tests.base_test import BaseTest


class PersonTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            person = PersonModel('test', 'test@test.com')
            person.save_to_db()
            telephone = TelephoneModel('000000000', 'comercial', 1)

            self.assertIsNone(TelephoneModel.find_by_number('000000000'), "Found an telephone with number "
                                                                          "'000000000' before save_to_db")

            telephone.save_to_db()

            self.assertIsNotNone(TelephoneModel.find_by_number('000000000'),
                                 "Did not find an telephone with number '000000000' after save_to_db")

            telephone.delete_from_db()

            self.assertIsNone(TelephoneModel.find_by_number('000000000'), "Found an telephone with "
                                                                          "number '000000000' after delete_from_db")

    def test_store_relationship(self):
        with self.app_context():
            person = PersonModel('test', 'test@test.com')
            telephone = TelephoneModel('000000000', 'comercial', 1)

            person.save_to_db()
            telephone.save_to_db()

            self.assertEqual(person.telephones[0].number, '000000000')
