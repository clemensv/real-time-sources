import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.weatherwarningeventenum import WeatherWarningEventEnum


class Test_WeatherWarningEventEnum(unittest.TestCase):
    """
    Test case for WeatherWarningEventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = WeatherWarningEventEnum.warning

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherWarningEventEnum
        """
        return WeatherWarningEventEnum.warning

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(WeatherWarningEventEnum.warning.value, 'warning')