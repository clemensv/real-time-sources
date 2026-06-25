"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hko_hong_kong_producer_data.weatherobservation import WeatherObservation
import datetime


class Test_WeatherObservation(unittest.TestCase):
    """
    Test case for WeatherObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherObservation for testing
        """
        instance = WeatherObservation(
            place_id='kmmdtdetrxkbxskbooyh',
            place_name='lgtyurfuvxkzohhlbkhs',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            temperature=float(87.49721207475719),
            rainfall_max=float(37.19868881547804),
            humidity=int(60),
            uv_index=float(13.882748764512298),
            uv_description='ijhkaphekvsaynwbbsun',
            district='lpncsnysvgstiarqmcim'
        )
        return instance

    
    def test_place_id_property(self):
        """
        Test place_id property
        """
        test_value = 'kmmdtdetrxkbxskbooyh'
        self.instance.place_id = test_value
        self.assertEqual(self.instance.place_id, test_value)
    
    def test_place_name_property(self):
        """
        Test place_name property
        """
        test_value = 'lgtyurfuvxkzohhlbkhs'
        self.instance.place_name = test_value
        self.assertEqual(self.instance.place_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(87.49721207475719)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_rainfall_max_property(self):
        """
        Test rainfall_max property
        """
        test_value = float(37.19868881547804)
        self.instance.rainfall_max = test_value
        self.assertEqual(self.instance.rainfall_max, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = int(60)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_uv_index_property(self):
        """
        Test uv_index property
        """
        test_value = float(13.882748764512298)
        self.instance.uv_index = test_value
        self.assertEqual(self.instance.uv_index, test_value)
    
    def test_uv_description_property(self):
        """
        Test uv_description property
        """
        test_value = 'ijhkaphekvsaynwbbsun'
        self.instance.uv_description = test_value
        self.assertEqual(self.instance.uv_description, test_value)
    
    def test_district_property(self):
        """
        Test district property
        """
        test_value = 'lpncsnysvgstiarqmcim'
        self.instance.district = test_value
        self.assertEqual(self.instance.district, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

