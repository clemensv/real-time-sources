"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from geosphere_austria_producer_data.at.geosphere.tawes.weatherobservation import WeatherObservation


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
            station_id='uckcgugejbefkfxsnfaa',
            observation_time='tutnvmeuvlnzgymeundk',
            temperature=float(75.61413444408645),
            humidity=float(15.484154858752442),
            precipitation=float(93.36289450119799),
            wind_direction=float(51.54213436609525),
            wind_speed=float(31.51146526687031),
            pressure=float(1.9385946682615507),
            sunshine_duration=float(17.676005496802038),
            global_radiation=float(63.266480585183075)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'uckcgugejbefkfxsnfaa'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'tutnvmeuvlnzgymeundk'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(75.61413444408645)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = float(15.484154858752442)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_precipitation_property(self):
        """
        Test precipitation property
        """
        test_value = float(93.36289450119799)
        self.instance.precipitation = test_value
        self.assertEqual(self.instance.precipitation, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(51.54213436609525)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(31.51146526687031)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(1.9385946682615507)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_sunshine_duration_property(self):
        """
        Test sunshine_duration property
        """
        test_value = float(17.676005496802038)
        self.instance.sunshine_duration = test_value
        self.assertEqual(self.instance.sunshine_duration, test_value)
    
    def test_global_radiation_property(self):
        """
        Test global_radiation property
        """
        test_value = float(63.266480585183075)
        self.instance.global_radiation = test_value
        self.assertEqual(self.instance.global_radiation, test_value)
    
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

