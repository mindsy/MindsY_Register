from datetime import datetime

from static.imports import *
from tests.unit.unit_base_test import UnitBaseTest


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        patient = PatientModel('test', 'test', 'canhoto', '00000000000', date, None, '00000000000', 'andamento')

        self.assertEqual(patient.scholarity, 'test',
                         "The scholarity of the patient after creation does not equal the constructor argument.")
        self.assertEqual(patient.observation, 'test',
                         "The observation of the patient after creation does not equal the constructor argument.")
        self.assertEqual(patient.manual_domain, 'canhoto',
                         "The manual domain of the patient after creation does not equal the constructor argument.")
        self.assertEqual(patient.registry_number_pat, '00000000000',
                         "The registry number's patient after creation does not equal the constructor argument.")
        self.assertEqual(patient.dt_birth, date,
                         "The dt_birth of the patient after creation does not equal the constructor argument.")
        self.assertEqual(patient.person_pat_id, None,
                         "The fk_person of the patient after creation does not equal the constructor argument.")
        self.assertEqual(patient.accountable_patient_registry_acc, '00000000000',
                         "The accountable patient registry number of the patient "
                         "after creation does not equal the constructor argument.")
        self.assertEqual(patient.status, 'andamento',
                         "The status of the patient after creation does not equal the constructor argument.")

