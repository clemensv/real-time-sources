"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from environment_canada_producer_data.weatherobservation import WeatherObservation
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
            msc_id='xbsjudjlotfvidlfwews',
            station_name='cpjlpatpojgegdtgxjqq',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            air_temperature=float(16.6756240323387),
            dew_point=float(24.65959397267782),
            relative_humidity=int(95),
            station_pressure=float(12.01517798550208),
            wind_speed=float(78.02313647627184),
            wind_direction=int(23),
            wind_gust=float(96.9010626447835),
            precipitation_1hr=float(37.62306264898078),
            mean_sea_level_pressure=float(48.8176012673486),
            visibility=float(54.59131388928705),
            snow_depth=float(72.13707228911706),
            total_cloud_cover=int(93),
            pressure_tendency_3hr=float(79.54588080913099),
            max_temperature_24hr=float(33.39503611389755),
            min_temperature_24hr=float(20.828915194960285),
            wind_speed_1hr=float(41.741304535282055),
            wind_gust_1hr=float(80.4151584685632),
            precipitation_24hr=float(92.76085378559075),
            altimeter_setting=float(8.215769465509926),
            province='ijhanndniclbacscmkwe'
        )
        return instance

    
    def test_msc_id_property(self):
        """
        Test msc_id property
        """
        test_value = 'xbsjudjlotfvidlfwews'
        self.instance.msc_id = test_value
        self.assertEqual(self.instance.msc_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'cpjlpatpojgegdtgxjqq'
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
        test_value = float(16.6756240323387)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_dew_point_property(self):
        """
        Test dew_point property
        """
        test_value = float(24.65959397267782)
        self.instance.dew_point = test_value
        self.assertEqual(self.instance.dew_point, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(95)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_station_pressure_property(self):
        """
        Test station_pressure property
        """
        test_value = float(12.01517798550208)
        self.instance.station_pressure = test_value
        self.assertEqual(self.instance.station_pressure, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(78.02313647627184)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = int(23)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(96.9010626447835)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_precipitation_1hr_property(self):
        """
        Test precipitation_1hr property
        """
        test_value = float(37.62306264898078)
        self.instance.precipitation_1hr = test_value
        self.assertEqual(self.instance.precipitation_1hr, test_value)
    
    def test_mean_sea_level_pressure_property(self):
        """
        Test mean_sea_level_pressure property
        """
        test_value = float(48.8176012673486)
        self.instance.mean_sea_level_pressure = test_value
        self.assertEqual(self.instance.mean_sea_level_pressure, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(54.59131388928705)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_snow_depth_property(self):
        """
        Test snow_depth property
        """
        test_value = float(72.13707228911706)
        self.instance.snow_depth = test_value
        self.assertEqual(self.instance.snow_depth, test_value)
    
    def test_total_cloud_cover_property(self):
        """
        Test total_cloud_cover property
        """
        test_value = int(93)
        self.instance.total_cloud_cover = test_value
        self.assertEqual(self.instance.total_cloud_cover, test_value)
    
    def test_pressure_tendency_3hr_property(self):
        """
        Test pressure_tendency_3hr property
        """
        test_value = float(79.54588080913099)
        self.instance.pressure_tendency_3hr = test_value
        self.assertEqual(self.instance.pressure_tendency_3hr, test_value)
    
    def test_max_temperature_24hr_property(self):
        """
        Test max_temperature_24hr property
        """
        test_value = float(33.39503611389755)
        self.instance.max_temperature_24hr = test_value
        self.assertEqual(self.instance.max_temperature_24hr, test_value)
    
    def test_min_temperature_24hr_property(self):
        """
        Test min_temperature_24hr property
        """
        test_value = float(20.828915194960285)
        self.instance.min_temperature_24hr = test_value
        self.assertEqual(self.instance.min_temperature_24hr, test_value)
    
    def test_wind_speed_1hr_property(self):
        """
        Test wind_speed_1hr property
        """
        test_value = float(41.741304535282055)
        self.instance.wind_speed_1hr = test_value
        self.assertEqual(self.instance.wind_speed_1hr, test_value)
    
    def test_wind_gust_1hr_property(self):
        """
        Test wind_gust_1hr property
        """
        test_value = float(80.4151584685632)
        self.instance.wind_gust_1hr = test_value
        self.assertEqual(self.instance.wind_gust_1hr, test_value)
    
    def test_precipitation_24hr_property(self):
        """
        Test precipitation_24hr property
        """
        test_value = float(92.76085378559075)
        self.instance.precipitation_24hr = test_value
        self.assertEqual(self.instance.precipitation_24hr, test_value)
    
    def test_altimeter_setting_property(self):
        """
        Test altimeter_setting property
        """
        test_value = float(8.215769465509926)
        self.instance.altimeter_setting = test_value
        self.assertEqual(self.instance.altimeter_setting, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'ijhanndniclbacscmkwe'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
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

