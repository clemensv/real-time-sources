import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_quake_amqp_producer_data.maxintensityenum import MaxIntensityenum


class Test_MaxIntensityenum(unittest.TestCase):
    """
    Test case for MaxIntensityenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = MaxIntensityenum.VALUE_1

    @staticmethod
    def create_instance():
        """
        Create instance of MaxIntensityenum
        """
        return MaxIntensityenum.VALUE_1

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(MaxIntensityenum.VALUE_1.value, '1')
        self.assertEqual(MaxIntensityenum.VALUE_2.value, '2')
        self.assertEqual(MaxIntensityenum.VALUE_3.value, '3')
        self.assertEqual(MaxIntensityenum.VALUE_4.value, '4')
        self.assertEqual(MaxIntensityenum.VALUE_5_MINUS.value, '5-')
        self.assertEqual(MaxIntensityenum.VALUE_5_PLUS.value, '5+')
        self.assertEqual(MaxIntensityenum.VALUE_6_MINUS.value, '6-')
        self.assertEqual(MaxIntensityenum.VALUE_6_PLUS.value, '6+')
        self.assertEqual(MaxIntensityenum.VALUE_7.value, '7')