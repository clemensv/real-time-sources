"""
Test case for MarineForecastPeriod
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_forecasts_producer_data.marineforecastperiod import MarineForecastPeriod


class Test_MarineForecastPeriod(unittest.TestCase):
    """
    Test case for MarineForecastPeriod
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MarineForecastPeriod.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MarineForecastPeriod for testing
        """
        instance = MarineForecastPeriod(
            period_name='qbiaunnqcdgjbtyyfqxj',
            forecast_text='stsuakyaovmqziixbbbf'
        )
        return instance

    
    def test_period_name_property(self):
        """
        Test period_name property
        """
        test_value = 'qbiaunnqcdgjbtyyfqxj'
        self.instance.period_name = test_value
        self.assertEqual(self.instance.period_name, test_value)
    
    def test_forecast_text_property(self):
        """
        Test forecast_text property
        """
        test_value = 'stsuakyaovmqziixbbbf'
        self.instance.forecast_text = test_value
        self.assertEqual(self.instance.forecast_text, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MarineForecastPeriod.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MarineForecastPeriod.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

