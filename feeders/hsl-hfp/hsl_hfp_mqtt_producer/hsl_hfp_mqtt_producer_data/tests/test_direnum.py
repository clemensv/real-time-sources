import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.hfp.direnum import DirEnum


class Test_DirEnum(unittest.TestCase):
    """
    Test case for DirEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = DirEnum.VALUE_1

    @staticmethod
    def create_instance():
        """
        Create instance of DirEnum
        """
        return DirEnum.VALUE_1

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(DirEnum.VALUE_1.value, '1')
        self.assertEqual(DirEnum.VALUE_2.value, '2')