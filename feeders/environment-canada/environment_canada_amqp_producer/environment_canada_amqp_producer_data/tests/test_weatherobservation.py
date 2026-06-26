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
            msc_id='lvdvnljvqkfihtlryhco',
            station_name='barmfrjunktdzquvfpne',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            air_temperature=float(10.50583526011768),
            dew_point=float(85.76976639887354),
            relative_humidity=int(76),
            station_pressure=float(84.62281765593478),
            wind_speed=float(96.01897998819044),
            wind_direction=int(14),
            wind_gust=float(71.11815437957848),
            precipitation_1hr=float(40.55950531957738),
            mean_sea_level_pressure=float(14.316977203827586),
            visibility=float(52.675039321818616),
            snow_depth=float(40.79296772536081),
            total_cloud_cover=int(3),
            pressure_tendency_3hr=float(84.33976164145261),
            max_temperature_24hr=float(53.03221445901529),
            min_temperature_24hr=float(67.66709228697275),
            wind_speed_1hr=float(22.909605431536527),
            wind_gust_1hr=float(84.54792210643606),
            precipitation_24hr=float(3.328179778657847),
            altimeter_setting=float(26.247187420727215),
            province='urswcmmgtnfyksepnocu'
        )
        return instance

    
    def test_msc_id_property(self):
        """
        Test msc_id property
        """
        test_value = 'lvdvnljvqkfihtlryhco'
        self.instance.msc_id = test_value
        self.assertEqual(self.instance.msc_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'barmfrjunktdzquvfpne'
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
        test_value = float(10.50583526011768)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_dew_point_property(self):
        """
        Test dew_point property
        """
        test_value = float(85.76976639887354)
        self.instance.dew_point = test_value
        self.assertEqual(self.instance.dew_point, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(76)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_station_pressure_property(self):
        """
        Test station_pressure property
        """
        test_value = float(84.62281765593478)
        self.instance.station_pressure = test_value
        self.assertEqual(self.instance.station_pressure, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(96.01897998819044)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = int(14)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(71.11815437957848)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_precipitation_1hr_property(self):
        """
        Test precipitation_1hr property
        """
        test_value = float(40.55950531957738)
        self.instance.precipitation_1hr = test_value
        self.assertEqual(self.instance.precipitation_1hr, test_value)
    
    def test_mean_sea_level_pressure_property(self):
        """
        Test mean_sea_level_pressure property
        """
        test_value = float(14.316977203827586)
        self.instance.mean_sea_level_pressure = test_value
        self.assertEqual(self.instance.mean_sea_level_pressure, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(52.675039321818616)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_snow_depth_property(self):
        """
        Test snow_depth property
        """
        test_value = float(40.79296772536081)
        self.instance.snow_depth = test_value
        self.assertEqual(self.instance.snow_depth, test_value)
    
    def test_total_cloud_cover_property(self):
        """
        Test total_cloud_cover property
        """
        test_value = int(3)
        self.instance.total_cloud_cover = test_value
        self.assertEqual(self.instance.total_cloud_cover, test_value)
    
    def test_pressure_tendency_3hr_property(self):
        """
        Test pressure_tendency_3hr property
        """
        test_value = float(84.33976164145261)
        self.instance.pressure_tendency_3hr = test_value
        self.assertEqual(self.instance.pressure_tendency_3hr, test_value)
    
    def test_max_temperature_24hr_property(self):
        """
        Test max_temperature_24hr property
        """
        test_value = float(53.03221445901529)
        self.instance.max_temperature_24hr = test_value
        self.assertEqual(self.instance.max_temperature_24hr, test_value)
    
    def test_min_temperature_24hr_property(self):
        """
        Test min_temperature_24hr property
        """
        test_value = float(67.66709228697275)
        self.instance.min_temperature_24hr = test_value
        self.assertEqual(self.instance.min_temperature_24hr, test_value)
    
    def test_wind_speed_1hr_property(self):
        """
        Test wind_speed_1hr property
        """
        test_value = float(22.909605431536527)
        self.instance.wind_speed_1hr = test_value
        self.assertEqual(self.instance.wind_speed_1hr, test_value)
    
    def test_wind_gust_1hr_property(self):
        """
        Test wind_gust_1hr property
        """
        test_value = float(84.54792210643606)
        self.instance.wind_gust_1hr = test_value
        self.assertEqual(self.instance.wind_gust_1hr, test_value)
    
    def test_precipitation_24hr_property(self):
        """
        Test precipitation_24hr property
        """
        test_value = float(3.328179778657847)
        self.instance.precipitation_24hr = test_value
        self.assertEqual(self.instance.precipitation_24hr, test_value)
    
    def test_altimeter_setting_property(self):
        """
        Test altimeter_setting property
        """
        test_value = float(26.247187420727215)
        self.instance.altimeter_setting = test_value
        self.assertEqual(self.instance.altimeter_setting, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'urswcmmgtnfyksepnocu'
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

