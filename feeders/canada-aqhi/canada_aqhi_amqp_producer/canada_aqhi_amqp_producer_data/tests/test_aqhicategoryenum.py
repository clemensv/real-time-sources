import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_aqhi_amqp_producer_data.ca.gc.weather.aqhi.aqhicategoryenum import AqhiCategoryenum


class Test_AqhiCategoryenum(unittest.TestCase):
    """
    Test case for AqhiCategoryenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = AqhiCategoryenum.Low

    @staticmethod
    def create_instance():
        """
        Create instance of AqhiCategoryenum
        """
        return AqhiCategoryenum.Low

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(AqhiCategoryenum.Low.value, 'Low')
        self.assertEqual(AqhiCategoryenum.Moderate.value, 'Moderate')
        self.assertEqual(AqhiCategoryenum.High.value, 'High')
        self.assertEqual(AqhiCategoryenum.Very_High.value, 'Very High')
        self.assertEqual(AqhiCategoryenum.Unknown.value, 'Unknown')