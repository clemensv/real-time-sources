"""
Test case for LandForecastPeriod
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_forecasts_producer_data.landforecastperiod import LandForecastPeriod


class Test_LandForecastPeriod(unittest.TestCase):
    """
    Test case for LandForecastPeriod
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LandForecastPeriod.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LandForecastPeriod for testing
        """
        instance = LandForecastPeriod(
            period_number=int(27),
            period_name='irxjxvxuemfyiylsqtui',
            detailed_forecast='cmmiabcjqzickchwwlun'
        )
        return instance

    
    def test_period_number_property(self):
        """
        Test period_number property
        """
        test_value = int(27)
        self.instance.period_number = test_value
        self.assertEqual(self.instance.period_number, test_value)
    
    def test_period_name_property(self):
        """
        Test period_name property
        """
        test_value = 'irxjxvxuemfyiylsqtui'
        self.instance.period_name = test_value
        self.assertEqual(self.instance.period_name, test_value)
    
    def test_detailed_forecast_property(self):
        """
        Test detailed_forecast property
        """
        test_value = 'cmmiabcjqzickchwwlun'
        self.instance.detailed_forecast = test_value
        self.assertEqual(self.instance.detailed_forecast, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LandForecastPeriod.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LandForecastPeriod.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

