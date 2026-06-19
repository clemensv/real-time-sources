"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from environment_canada_amqp_producer_data.weatherobservation import WeatherObservation
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
            msc_id='xdgfarkmxbmjjkfcelto',
            station_name='rgjabotlzypkkmnqhxbb',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            air_temperature=float(98.77431896724835),
            dew_point=float(48.93948856230571),
            relative_humidity=int(97),
            station_pressure=float(55.99709121639711),
            wind_speed=float(46.47739211006302),
            wind_direction=int(1),
            wind_gust=float(49.23674239532987),
            precipitation_1hr=float(91.32186529469347),
            mean_sea_level_pressure=float(48.90490755352796),
            visibility=float(6.01887416740412),
            snow_depth=float(71.69832995559624),
            total_cloud_cover=int(90),
            pressure_tendency_3hr=float(5.392831789080854),
            max_temperature_24hr=float(9.562558842695223),
            min_temperature_24hr=float(66.81679778451385),
            wind_speed_1hr=float(53.69680539298949),
            wind_gust_1hr=float(72.21338837176032),
            precipitation_24hr=float(47.02512954178651),
            altimeter_setting=float(31.907572238194714),
            province='hvhtpsuggwplaxanfdzw'
        )
        return instance

    
    def test_msc_id_property(self):
        """
        Test msc_id property
        """
        test_value = 'xdgfarkmxbmjjkfcelto'
        self.instance.msc_id = test_value
        self.assertEqual(self.instance.msc_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'rgjabotlzypkkmnqhxbb'
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
        test_value = float(98.77431896724835)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_dew_point_property(self):
        """
        Test dew_point property
        """
        test_value = float(48.93948856230571)
        self.instance.dew_point = test_value
        self.assertEqual(self.instance.dew_point, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(97)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_station_pressure_property(self):
        """
        Test station_pressure property
        """
        test_value = float(55.99709121639711)
        self.instance.station_pressure = test_value
        self.assertEqual(self.instance.station_pressure, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(46.47739211006302)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = int(1)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(49.23674239532987)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_precipitation_1hr_property(self):
        """
        Test precipitation_1hr property
        """
        test_value = float(91.32186529469347)
        self.instance.precipitation_1hr = test_value
        self.assertEqual(self.instance.precipitation_1hr, test_value)
    
    def test_mean_sea_level_pressure_property(self):
        """
        Test mean_sea_level_pressure property
        """
        test_value = float(48.90490755352796)
        self.instance.mean_sea_level_pressure = test_value
        self.assertEqual(self.instance.mean_sea_level_pressure, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(6.01887416740412)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_snow_depth_property(self):
        """
        Test snow_depth property
        """
        test_value = float(71.69832995559624)
        self.instance.snow_depth = test_value
        self.assertEqual(self.instance.snow_depth, test_value)
    
    def test_total_cloud_cover_property(self):
        """
        Test total_cloud_cover property
        """
        test_value = int(90)
        self.instance.total_cloud_cover = test_value
        self.assertEqual(self.instance.total_cloud_cover, test_value)
    
    def test_pressure_tendency_3hr_property(self):
        """
        Test pressure_tendency_3hr property
        """
        test_value = float(5.392831789080854)
        self.instance.pressure_tendency_3hr = test_value
        self.assertEqual(self.instance.pressure_tendency_3hr, test_value)
    
    def test_max_temperature_24hr_property(self):
        """
        Test max_temperature_24hr property
        """
        test_value = float(9.562558842695223)
        self.instance.max_temperature_24hr = test_value
        self.assertEqual(self.instance.max_temperature_24hr, test_value)
    
    def test_min_temperature_24hr_property(self):
        """
        Test min_temperature_24hr property
        """
        test_value = float(66.81679778451385)
        self.instance.min_temperature_24hr = test_value
        self.assertEqual(self.instance.min_temperature_24hr, test_value)
    
    def test_wind_speed_1hr_property(self):
        """
        Test wind_speed_1hr property
        """
        test_value = float(53.69680539298949)
        self.instance.wind_speed_1hr = test_value
        self.assertEqual(self.instance.wind_speed_1hr, test_value)
    
    def test_wind_gust_1hr_property(self):
        """
        Test wind_gust_1hr property
        """
        test_value = float(72.21338837176032)
        self.instance.wind_gust_1hr = test_value
        self.assertEqual(self.instance.wind_gust_1hr, test_value)
    
    def test_precipitation_24hr_property(self):
        """
        Test precipitation_24hr property
        """
        test_value = float(47.02512954178651)
        self.instance.precipitation_24hr = test_value
        self.assertEqual(self.instance.precipitation_24hr, test_value)
    
    def test_altimeter_setting_property(self):
        """
        Test altimeter_setting property
        """
        test_value = float(31.907572238194714)
        self.instance.altimeter_setting = test_value
        self.assertEqual(self.instance.altimeter_setting, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'hvhtpsuggwplaxanfdzw'
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

