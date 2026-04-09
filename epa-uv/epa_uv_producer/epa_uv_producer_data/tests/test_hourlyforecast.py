"""
Test case for HourlyForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from epa_uv_producer_data.hourlyforecast import HourlyForecast


class Test_HourlyForecast(unittest.TestCase):
    """
    Test case for HourlyForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_HourlyForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of HourlyForecast for testing
        """
        instance = HourlyForecast(
            location_id='mhdngkspejionsaolqqn',
            city='vyqiryfkxojalgcrmvid',
            state='qwnztsbzlozeblziwymo',
            forecast_datetime='gejgklxrcvlqtufvyvez',
            uv_index=int(10)
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = 'mhdngkspejionsaolqqn'
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_city_property(self):
        """
        Test city property
        """
        test_value = 'vyqiryfkxojalgcrmvid'
        self.instance.city = test_value
        self.assertEqual(self.instance.city, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'qwnztsbzlozeblziwymo'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_forecast_datetime_property(self):
        """
        Test forecast_datetime property
        """
        test_value = 'gejgklxrcvlqtufvyvez'
        self.instance.forecast_datetime = test_value
        self.assertEqual(self.instance.forecast_datetime, test_value)
    
    def test_uv_index_property(self):
        """
        Test uv_index property
        """
        test_value = int(10)
        self.instance.uv_index = test_value
        self.assertEqual(self.instance.uv_index, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = HourlyForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = HourlyForecast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

