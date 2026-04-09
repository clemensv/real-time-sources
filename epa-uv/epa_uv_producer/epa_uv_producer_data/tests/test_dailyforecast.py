"""
Test case for DailyForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from epa_uv_producer_data.dailyforecast import DailyForecast


class Test_DailyForecast(unittest.TestCase):
    """
    Test case for DailyForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DailyForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DailyForecast for testing
        """
        instance = DailyForecast(
            location_id='tuimcyrnovsnxrxwmxsy',
            city='sittjdlzwzcmusfybqfr',
            state='aewrpavnyfxeftesfiib',
            forecast_date='jfqtumcigicnamdznaci',
            uv_index=int(71),
            uv_alert='mldahjadlrxxgkdvbvna'
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = 'tuimcyrnovsnxrxwmxsy'
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_city_property(self):
        """
        Test city property
        """
        test_value = 'sittjdlzwzcmusfybqfr'
        self.instance.city = test_value
        self.assertEqual(self.instance.city, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'aewrpavnyfxeftesfiib'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_forecast_date_property(self):
        """
        Test forecast_date property
        """
        test_value = 'jfqtumcigicnamdznaci'
        self.instance.forecast_date = test_value
        self.assertEqual(self.instance.forecast_date, test_value)
    
    def test_uv_index_property(self):
        """
        Test uv_index property
        """
        test_value = int(71)
        self.instance.uv_index = test_value
        self.assertEqual(self.instance.uv_index, test_value)
    
    def test_uv_alert_property(self):
        """
        Test uv_alert property
        """
        test_value = 'mldahjadlrxxgkdvbvna'
        self.instance.uv_alert = test_value
        self.assertEqual(self.instance.uv_alert, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DailyForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DailyForecast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

