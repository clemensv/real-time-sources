"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kmi_belgium_producer_data.weatherobservation import WeatherObservation
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
            station_code='lhkaturuadlwzofonuoh',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            precip_quantity=float(77.4313707038458),
            temp_dry_shelter_avg=float(39.766553695254345),
            temp_grass_pt100_avg=float(75.49944422472863),
            temp_soil_avg=float(31.180091874135318),
            temp_soil_avg_5cm=float(92.98092927233876),
            temp_soil_avg_10cm=float(99.23621710202292),
            temp_soil_avg_20cm=float(54.137601128331944),
            temp_soil_avg_50cm=float(84.79829328390048),
            wind_speed_10m=float(56.61531117277596),
            wind_speed_avg_30m=float(44.01250464486287),
            wind_direction=float(21.09330419578088),
            wind_gusts_speed=float(56.4001905075924),
            humidity_rel_shelter_avg=float(8.531321533904979),
            pressure=float(0.07402826384610428),
            sun_duration=float(18.870394675630052),
            short_wave_from_sky_avg=float(41.04216622019917),
            sun_int_avg=float(28.873213968184363),
            region='ddeqvndyluhauwnsnmix'
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'lhkaturuadlwzofonuoh'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_precip_quantity_property(self):
        """
        Test precip_quantity property
        """
        test_value = float(77.4313707038458)
        self.instance.precip_quantity = test_value
        self.assertEqual(self.instance.precip_quantity, test_value)
    
    def test_temp_dry_shelter_avg_property(self):
        """
        Test temp_dry_shelter_avg property
        """
        test_value = float(39.766553695254345)
        self.instance.temp_dry_shelter_avg = test_value
        self.assertEqual(self.instance.temp_dry_shelter_avg, test_value)
    
    def test_temp_grass_pt100_avg_property(self):
        """
        Test temp_grass_pt100_avg property
        """
        test_value = float(75.49944422472863)
        self.instance.temp_grass_pt100_avg = test_value
        self.assertEqual(self.instance.temp_grass_pt100_avg, test_value)
    
    def test_temp_soil_avg_property(self):
        """
        Test temp_soil_avg property
        """
        test_value = float(31.180091874135318)
        self.instance.temp_soil_avg = test_value
        self.assertEqual(self.instance.temp_soil_avg, test_value)
    
    def test_temp_soil_avg_5cm_property(self):
        """
        Test temp_soil_avg_5cm property
        """
        test_value = float(92.98092927233876)
        self.instance.temp_soil_avg_5cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_5cm, test_value)
    
    def test_temp_soil_avg_10cm_property(self):
        """
        Test temp_soil_avg_10cm property
        """
        test_value = float(99.23621710202292)
        self.instance.temp_soil_avg_10cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_10cm, test_value)
    
    def test_temp_soil_avg_20cm_property(self):
        """
        Test temp_soil_avg_20cm property
        """
        test_value = float(54.137601128331944)
        self.instance.temp_soil_avg_20cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_20cm, test_value)
    
    def test_temp_soil_avg_50cm_property(self):
        """
        Test temp_soil_avg_50cm property
        """
        test_value = float(84.79829328390048)
        self.instance.temp_soil_avg_50cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_50cm, test_value)
    
    def test_wind_speed_10m_property(self):
        """
        Test wind_speed_10m property
        """
        test_value = float(56.61531117277596)
        self.instance.wind_speed_10m = test_value
        self.assertEqual(self.instance.wind_speed_10m, test_value)
    
    def test_wind_speed_avg_30m_property(self):
        """
        Test wind_speed_avg_30m property
        """
        test_value = float(44.01250464486287)
        self.instance.wind_speed_avg_30m = test_value
        self.assertEqual(self.instance.wind_speed_avg_30m, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(21.09330419578088)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gusts_speed_property(self):
        """
        Test wind_gusts_speed property
        """
        test_value = float(56.4001905075924)
        self.instance.wind_gusts_speed = test_value
        self.assertEqual(self.instance.wind_gusts_speed, test_value)
    
    def test_humidity_rel_shelter_avg_property(self):
        """
        Test humidity_rel_shelter_avg property
        """
        test_value = float(8.531321533904979)
        self.instance.humidity_rel_shelter_avg = test_value
        self.assertEqual(self.instance.humidity_rel_shelter_avg, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(0.07402826384610428)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_sun_duration_property(self):
        """
        Test sun_duration property
        """
        test_value = float(18.870394675630052)
        self.instance.sun_duration = test_value
        self.assertEqual(self.instance.sun_duration, test_value)
    
    def test_short_wave_from_sky_avg_property(self):
        """
        Test short_wave_from_sky_avg property
        """
        test_value = float(41.04216622019917)
        self.instance.short_wave_from_sky_avg = test_value
        self.assertEqual(self.instance.short_wave_from_sky_avg, test_value)
    
    def test_sun_int_avg_property(self):
        """
        Test sun_int_avg property
        """
        test_value = float(28.873213968184363)
        self.instance.sun_int_avg = test_value
        self.assertEqual(self.instance.sun_int_avg, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'ddeqvndyluhauwnsnmix'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
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

