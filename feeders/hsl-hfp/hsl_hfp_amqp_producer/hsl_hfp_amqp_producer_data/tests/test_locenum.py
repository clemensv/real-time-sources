import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_amqp_producer_data.fi.hsl.hfp.locenum import LocEnum


class Test_LocEnum(unittest.TestCase):
    """
    Test case for LocEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = LocEnum.GPS

    @staticmethod
    def create_instance():
        """
        Create instance of LocEnum
        """
        return LocEnum.GPS

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(LocEnum.GPS.value, 'GPS')
        self.assertEqual(LocEnum.ODO.value, 'ODO')
        self.assertEqual(LocEnum.MAN.value, 'MAN')
        self.assertEqual(LocEnum.DR.value, 'DR')
        self.assertEqual(LocEnum.N_SLASHA.value, 'N/A')