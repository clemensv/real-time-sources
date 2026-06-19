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
            station_code='kzyykkqzedjwtnzqtgqu',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            precip_quantity=float(78.50513226710025),
            temp_dry_shelter_avg=float(42.28760926905664),
            temp_grass_pt100_avg=float(44.374940939020014),
            temp_soil_avg=float(50.68547679876172),
            temp_soil_avg_5cm=float(82.51023284101542),
            temp_soil_avg_10cm=float(69.64295787996168),
            temp_soil_avg_20cm=float(76.51297939740626),
            temp_soil_avg_50cm=float(60.925792433861325),
            wind_speed_10m=float(17.939429370279836),
            wind_speed_avg_30m=float(80.11226759864873),
            wind_direction=float(9.562567430985547),
            wind_gusts_speed=float(57.14248620522293),
            humidity_rel_shelter_avg=float(34.67361469467348),
            pressure=float(42.61131649261887),
            sun_duration=float(24.560954763528542),
            short_wave_from_sky_avg=float(92.39230359912685),
            sun_int_avg=float(45.07269973976066),
            region='hjsrptufpuqnmuhyvleu'
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'kzyykkqzedjwtnzqtgqu'
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
        test_value = float(78.50513226710025)
        self.instance.precip_quantity = test_value
        self.assertEqual(self.instance.precip_quantity, test_value)
    
    def test_temp_dry_shelter_avg_property(self):
        """
        Test temp_dry_shelter_avg property
        """
        test_value = float(42.28760926905664)
        self.instance.temp_dry_shelter_avg = test_value
        self.assertEqual(self.instance.temp_dry_shelter_avg, test_value)
    
    def test_temp_grass_pt100_avg_property(self):
        """
        Test temp_grass_pt100_avg property
        """
        test_value = float(44.374940939020014)
        self.instance.temp_grass_pt100_avg = test_value
        self.assertEqual(self.instance.temp_grass_pt100_avg, test_value)
    
    def test_temp_soil_avg_property(self):
        """
        Test temp_soil_avg property
        """
        test_value = float(50.68547679876172)
        self.instance.temp_soil_avg = test_value
        self.assertEqual(self.instance.temp_soil_avg, test_value)
    
    def test_temp_soil_avg_5cm_property(self):
        """
        Test temp_soil_avg_5cm property
        """
        test_value = float(82.51023284101542)
        self.instance.temp_soil_avg_5cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_5cm, test_value)
    
    def test_temp_soil_avg_10cm_property(self):
        """
        Test temp_soil_avg_10cm property
        """
        test_value = float(69.64295787996168)
        self.instance.temp_soil_avg_10cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_10cm, test_value)
    
    def test_temp_soil_avg_20cm_property(self):
        """
        Test temp_soil_avg_20cm property
        """
        test_value = float(76.51297939740626)
        self.instance.temp_soil_avg_20cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_20cm, test_value)
    
    def test_temp_soil_avg_50cm_property(self):
        """
        Test temp_soil_avg_50cm property
        """
        test_value = float(60.925792433861325)
        self.instance.temp_soil_avg_50cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_50cm, test_value)
    
    def test_wind_speed_10m_property(self):
        """
        Test wind_speed_10m property
        """
        test_value = float(17.939429370279836)
        self.instance.wind_speed_10m = test_value
        self.assertEqual(self.instance.wind_speed_10m, test_value)
    
    def test_wind_speed_avg_30m_property(self):
        """
        Test wind_speed_avg_30m property
        """
        test_value = float(80.11226759864873)
        self.instance.wind_speed_avg_30m = test_value
        self.assertEqual(self.instance.wind_speed_avg_30m, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(9.562567430985547)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gusts_speed_property(self):
        """
        Test wind_gusts_speed property
        """
        test_value = float(57.14248620522293)
        self.instance.wind_gusts_speed = test_value
        self.assertEqual(self.instance.wind_gusts_speed, test_value)
    
    def test_humidity_rel_shelter_avg_property(self):
        """
        Test humidity_rel_shelter_avg property
        """
        test_value = float(34.67361469467348)
        self.instance.humidity_rel_shelter_avg = test_value
        self.assertEqual(self.instance.humidity_rel_shelter_avg, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(42.61131649261887)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_sun_duration_property(self):
        """
        Test sun_duration property
        """
        test_value = float(24.560954763528542)
        self.instance.sun_duration = test_value
        self.assertEqual(self.instance.sun_duration, test_value)
    
    def test_short_wave_from_sky_avg_property(self):
        """
        Test short_wave_from_sky_avg property
        """
        test_value = float(92.39230359912685)
        self.instance.short_wave_from_sky_avg = test_value
        self.assertEqual(self.instance.short_wave_from_sky_avg, test_value)
    
    def test_sun_int_avg_property(self):
        """
        Test sun_int_avg property
        """
        test_value = float(45.07269973976066)
        self.instance.sun_int_avg = test_value
        self.assertEqual(self.instance.sun_int_avg, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'hjsrptufpuqnmuhyvleu'
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

