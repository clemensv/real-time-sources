"""
Test case for DailyForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from epa_uv_amqp_producer_data.dailyforecast import DailyForecast


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
            location_id='ibeokfyjimgrorsviqtr',
            city='mhofevklwrtnctcrbccu',
            state='vwywfzboxybupzomsrrx',
            forecast_date='borfdbrbcugkrqhiiwip',
            uv_index=int(40),
            uv_alert='agmvbqguyapskjuyookh',
            city_slug='ooyjnkiyzjpsnzukllca'
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = 'ibeokfyjimgrorsviqtr'
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_city_property(self):
        """
        Test city property
        """
        test_value = 'mhofevklwrtnctcrbccu'
        self.instance.city = test_value
        self.assertEqual(self.instance.city, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'vwywfzboxybupzomsrrx'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_forecast_date_property(self):
        """
        Test forecast_date property
        """
        test_value = 'borfdbrbcugkrqhiiwip'
        self.instance.forecast_date = test_value
        self.assertEqual(self.instance.forecast_date, test_value)
    
    def test_uv_index_property(self):
        """
        Test uv_index property
        """
        test_value = int(40)
        self.instance.uv_index = test_value
        self.assertEqual(self.instance.uv_index, test_value)
    
    def test_uv_alert_property(self):
        """
        Test uv_alert property
        """
        test_value = 'agmvbqguyapskjuyookh'
        self.instance.uv_alert = test_value
        self.assertEqual(self.instance.uv_alert, test_value)
    
    def test_city_slug_property(self):
        """
        Test city_slug property
        """
        test_value = 'ooyjnkiyzjpsnzukllca'
        self.instance.city_slug = test_value
        self.assertEqual(self.instance.city_slug, test_value)
    
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

