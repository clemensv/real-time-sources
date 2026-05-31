import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nasa_firms_mqtt_producer_data.nasa.firms.daynightenum import DaynightEnum


class Test_DaynightEnum(unittest.TestCase):
    """
    Test case for DaynightEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = DaynightEnum.D

    @staticmethod
    def create_instance():
        """
        Create instance of DaynightEnum
        """
        return DaynightEnum.D

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(DaynightEnum.D.value, 'D')
        self.assertEqual(DaynightEnum.N.value, 'N')