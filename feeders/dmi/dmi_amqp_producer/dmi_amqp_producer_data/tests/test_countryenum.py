import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_amqp_producer_data.countryenum import CountryEnum


class Test_CountryEnum(unittest.TestCase):
    """
    Test case for CountryEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = CountryEnum.DNK

    @staticmethod
    def create_instance():
        """
        Create instance of CountryEnum
        """
        return CountryEnum.DNK

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(CountryEnum.DNK.value, 'DNK')
        self.assertEqual(CountryEnum.GRL.value, 'GRL')
        self.assertEqual(CountryEnum.FRO.value, 'FRO')