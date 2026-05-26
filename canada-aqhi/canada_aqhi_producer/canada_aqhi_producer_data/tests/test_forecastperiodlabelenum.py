import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_aqhi_producer_data.ca.gc.weather.aqhi.forecastperiodlabelenum import ForecastPeriodLabelenum


class Test_ForecastPeriodLabelenum(unittest.TestCase):
    """
    Test case for ForecastPeriodLabelenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ForecastPeriodLabelenum.Today

    @staticmethod
    def create_instance():
        """
        Create instance of ForecastPeriodLabelenum
        """
        return ForecastPeriodLabelenum.Today

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ForecastPeriodLabelenum.Today.value, 'Today')
        self.assertEqual(ForecastPeriodLabelenum.Tonight.value, 'Tonight')
        self.assertEqual(ForecastPeriodLabelenum.Tomorrow.value, 'Tomorrow')
        self.assertEqual(ForecastPeriodLabelenum.Tomorrow_Night.value, 'Tomorrow Night')