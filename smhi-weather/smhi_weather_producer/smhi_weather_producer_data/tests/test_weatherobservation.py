"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from smhi_weather_producer_data.weatherobservation import WeatherObservation
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
            station_id='fthtuzcwncrnkclzqqme',
            station_name='sqsktssbwgquawfamgdc',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            air_temperature=float(64.5441699428818),
            wind_gust=float(38.23184509675938),
            dew_point=float(54.93410678058955),
            air_pressure=float(6.359459132231793),
            relative_humidity=int(76),
            precipitation_last_hour=float(17.581222680062623),
            wind_direction=float(85.53436150630421),
            wind_speed=float(5.24440973321052),
            max_wind_speed=float(50.16910145375015),
            visibility=float(43.69004223271664),
            total_cloud_cover=int(37),
            present_weather=int(81),
            sunshine_duration=float(97.76537147210188),
            global_irradiance=float(34.07089640340112),
            precipitation_intensity=float(86.4539701294217),
            quality='inosktkrsfusrscvvmfv'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fthtuzcwncrnkclzqqme'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'sqsktssbwgquawfamgdc'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(64.5441699428818)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(38.23184509675938)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_dew_point_property(self):
        """
        Test dew_point property
        """
        test_value = float(54.93410678058955)
        self.instance.dew_point = test_value
        self.assertEqual(self.instance.dew_point, test_value)
    
    def test_air_pressure_property(self):
        """
        Test air_pressure property
        """
        test_value = float(6.359459132231793)
        self.instance.air_pressure = test_value
        self.assertEqual(self.instance.air_pressure, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(76)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_precipitation_last_hour_property(self):
        """
        Test precipitation_last_hour property
        """
        test_value = float(17.581222680062623)
        self.instance.precipitation_last_hour = test_value
        self.assertEqual(self.instance.precipitation_last_hour, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(85.53436150630421)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(5.24440973321052)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_max_wind_speed_property(self):
        """
        Test max_wind_speed property
        """
        test_value = float(50.16910145375015)
        self.instance.max_wind_speed = test_value
        self.assertEqual(self.instance.max_wind_speed, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(43.69004223271664)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_total_cloud_cover_property(self):
        """
        Test total_cloud_cover property
        """
        test_value = int(37)
        self.instance.total_cloud_cover = test_value
        self.assertEqual(self.instance.total_cloud_cover, test_value)
    
    def test_present_weather_property(self):
        """
        Test present_weather property
        """
        test_value = int(81)
        self.instance.present_weather = test_value
        self.assertEqual(self.instance.present_weather, test_value)
    
    def test_sunshine_duration_property(self):
        """
        Test sunshine_duration property
        """
        test_value = float(97.76537147210188)
        self.instance.sunshine_duration = test_value
        self.assertEqual(self.instance.sunshine_duration, test_value)
    
    def test_global_irradiance_property(self):
        """
        Test global_irradiance property
        """
        test_value = float(34.07089640340112)
        self.instance.global_irradiance = test_value
        self.assertEqual(self.instance.global_irradiance, test_value)
    
    def test_precipitation_intensity_property(self):
        """
        Test precipitation_intensity property
        """
        test_value = float(86.4539701294217)
        self.instance.precipitation_intensity = test_value
        self.assertEqual(self.instance.precipitation_intensity, test_value)
    
    def test_quality_property(self):
        """
        Test quality property
        """
        test_value = 'inosktkrsfusrscvvmfv'
        self.instance.quality = test_value
        self.assertEqual(self.instance.quality, test_value)
    
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

