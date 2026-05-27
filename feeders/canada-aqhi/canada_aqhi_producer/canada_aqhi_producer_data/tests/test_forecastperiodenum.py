import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_aqhi_producer_data.ca.gc.weather.aqhi.forecastperiodenum import ForecastPeriodenum


class Test_ForecastPeriodenum(unittest.TestCase):
    """
    Test case for ForecastPeriodenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ForecastPeriodenum.VALUE_1

    @staticmethod
    def create_instance():
        """
        Create instance of ForecastPeriodenum
        """
        return ForecastPeriodenum.VALUE_1

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ForecastPeriodenum.VALUE_1.value, 1)
        self.assertEqual(ForecastPeriodenum.VALUE_2.value, 2)
        self.assertEqual(ForecastPeriodenum.VALUE_3.value, 3)
        self.assertEqual(ForecastPeriodenum.VALUE_4.value, 4)