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
            station_id='iogcurhxaamdaolxwkia',
            observation_time='khwnprszpysovqnsjige',
            temperature=float(59.68475662236678),
            humidity=float(11.54020285020878),
            precipitation=float(94.86738871723152),
            wind_direction=float(94.70818121749195),
            wind_speed=float(10.933813282236882),
            pressure=float(87.95359806904787),
            sunshine_duration=float(72.81161435802927),
            global_radiation=float(11.656342792828333)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'iogcurhxaamdaolxwkia'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'khwnprszpysovqnsjige'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(59.68475662236678)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = float(11.54020285020878)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_precipitation_property(self):
        """
        Test precipitation property
        """
        test_value = float(94.86738871723152)
        self.instance.precipitation = test_value
        self.assertEqual(self.instance.precipitation, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(94.70818121749195)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(10.933813282236882)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(87.95359806904787)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_sunshine_duration_property(self):
        """
        Test sunshine_duration property
        """
        test_value = float(72.81161435802927)
        self.instance.sunshine_duration = test_value
        self.assertEqual(self.instance.sunshine_duration, test_value)
    
    def test_global_radiation_property(self):
        """
        Test global_radiation property
        """
        test_value = float(11.656342792828333)
        self.instance.global_radiation = test_value
        self.assertEqual(self.instance.global_radiation, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
