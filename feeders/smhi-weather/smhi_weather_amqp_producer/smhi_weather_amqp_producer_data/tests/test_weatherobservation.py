"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from smhi_weather_amqp_producer_data.weatherobservation import WeatherObservation
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
            station_id='lngcvwnjkqmczeimkzts',
            station_name='avezfvutliqgfjboivvk',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            air_temperature=float(42.18127265752073),
            wind_gust=float(43.71573056759932),
            dew_point=float(53.28225235726298),
            air_pressure=float(57.108748998177205),
            relative_humidity=int(6),
            precipitation_last_hour=float(16.65146789258789),
            wind_direction=float(75.40403109797394),
            wind_speed=float(5.322286952478028),
            max_wind_speed=float(26.66360313891305),
            visibility=float(79.27281205146882),
            total_cloud_cover=int(34),
            present_weather=int(73),
            sunshine_duration=float(72.22444176800012),
            global_irradiance=float(65.56325861735326),
            precipitation_intensity=float(91.17631315016635),
            quality='cznevnqutsrgtlsdtehm',
            lan='eqwfxkfkxpbqnmtfizyp'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'lngcvwnjkqmczeimkzts'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'avezfvutliqgfjboivvk'
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
        test_value = float(42.18127265752073)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(43.71573056759932)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_dew_point_property(self):
        """
        Test dew_point property
        """
        test_value = float(53.28225235726298)
        self.instance.dew_point = test_value
        self.assertEqual(self.instance.dew_point, test_value)
    
    def test_air_pressure_property(self):
        """
        Test air_pressure property
        """
        test_value = float(57.108748998177205)
        self.instance.air_pressure = test_value
        self.assertEqual(self.instance.air_pressure, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(6)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_precipitation_last_hour_property(self):
        """
        Test precipitation_last_hour property
        """
        test_value = float(16.65146789258789)
        self.instance.precipitation_last_hour = test_value
        self.assertEqual(self.instance.precipitation_last_hour, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(75.40403109797394)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(5.322286952478028)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_max_wind_speed_property(self):
        """
        Test max_wind_speed property
        """
        test_value = float(26.66360313891305)
        self.instance.max_wind_speed = test_value
        self.assertEqual(self.instance.max_wind_speed, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(79.27281205146882)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_total_cloud_cover_property(self):
        """
        Test total_cloud_cover property
        """
        test_value = int(34)
        self.instance.total_cloud_cover = test_value
        self.assertEqual(self.instance.total_cloud_cover, test_value)
    
    def test_present_weather_property(self):
        """
        Test present_weather property
        """
        test_value = int(73)
        self.instance.present_weather = test_value
        self.assertEqual(self.instance.present_weather, test_value)
    
    def test_sunshine_duration_property(self):
        """
        Test sunshine_duration property
        """
        test_value = float(72.22444176800012)
        self.instance.sunshine_duration = test_value
        self.assertEqual(self.instance.sunshine_duration, test_value)
    
    def test_global_irradiance_property(self):
        """
        Test global_irradiance property
        """
        test_value = float(65.56325861735326)
        self.instance.global_irradiance = test_value
        self.assertEqual(self.instance.global_irradiance, test_value)
    
    def test_precipitation_intensity_property(self):
        """
        Test precipitation_intensity property
        """
        test_value = float(91.17631315016635)
        self.instance.precipitation_intensity = test_value
        self.assertEqual(self.instance.precipitation_intensity, test_value)
    
    def test_quality_property(self):
        """
        Test quality property
        """
        test_value = 'cznevnqutsrgtlsdtehm'
        self.instance.quality = test_value
        self.assertEqual(self.instance.quality, test_value)
    
    def test_lan_property(self):
        """
        Test lan property
        """
        test_value = 'eqwfxkfkxpbqnmtfizyp'
        self.instance.lan = test_value
        self.assertEqual(self.instance.lan, test_value)
    
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

