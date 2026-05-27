import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_mqtt_producer_data.de.wsv.pegelonline.trendenum import TrendEnum


class Test_TrendEnum(unittest.TestCase):
    """
    Test case for TrendEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TrendEnum.VALUE_NEG_1

    @staticmethod
    def create_instance():
        """
        Create instance of TrendEnum
        """
        return TrendEnum.VALUE_NEG_1

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TrendEnum.VALUE_NEG_1.value, -1)
        self.assertEqual(TrendEnum.VALUE_0.value, 0)
        self.assertEqual(TrendEnum.VALUE_1.value, 1)