import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_amqp_producer_data.uk.kcl.laqn.airqualitybandenum import AirQualityBandenum


class Test_AirQualityBandenum(unittest.TestCase):
    """
    Test case for AirQualityBandenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = AirQualityBandenum.Low

    @staticmethod
    def create_instance():
        """
        Create instance of AirQualityBandenum
        """
        return AirQualityBandenum.Low

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(AirQualityBandenum.Low.value, 'Low')
        self.assertEqual(AirQualityBandenum.Moderate.value, 'Moderate')
        self.assertEqual(AirQualityBandenum.High.value, 'High')
        self.assertEqual(AirQualityBandenum.Very_High.value, 'Very High')