import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_mqtt_producer_data.officetypeenum import OfficeTypeenum


class Test_OfficeTypeenum(unittest.TestCase):
    """
    Test case for OfficeTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = OfficeTypeenum.PREFECTURE

    @staticmethod
    def create_instance():
        """
        Create instance of OfficeTypeenum
        """
        return OfficeTypeenum.PREFECTURE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(OfficeTypeenum.PREFECTURE.value, 'PREFECTURE')
        self.assertEqual(OfficeTypeenum.SUBREGION.value, 'SUBREGION')
        self.assertEqual(OfficeTypeenum.OFFICE.value, 'OFFICE')