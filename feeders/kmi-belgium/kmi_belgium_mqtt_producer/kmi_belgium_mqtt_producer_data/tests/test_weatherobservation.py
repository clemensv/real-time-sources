"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kmi_belgium_mqtt_producer_data.weatherobservation import WeatherObservation
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
            station_code='fxxebgynqsiimkxbbjba',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            precip_quantity=float(10.961287887309378),
            temp_dry_shelter_avg=float(3.1993786447440775),
            temp_grass_pt100_avg=float(60.55034204459707),
            temp_soil_avg=float(47.75924100768082),
            temp_soil_avg_5cm=float(92.96607799500227),
            temp_soil_avg_10cm=float(0.22598038735198722),
            temp_soil_avg_20cm=float(64.50842024928875),
            temp_soil_avg_50cm=float(74.20229221702492),
            wind_speed_10m=float(67.76297452608567),
            wind_speed_avg_30m=float(99.16252700378118),
            wind_direction=float(65.38948206643545),
            wind_gusts_speed=float(62.40356303135023),
            humidity_rel_shelter_avg=float(55.29522160490193),
            pressure=float(25.939443530480986),
            sun_duration=float(36.60873821866857),
            short_wave_from_sky_avg=float(33.183670556294956),
            sun_int_avg=float(35.18478090168323),
            region='zstitvmwpwvlklkogwzc'
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'fxxebgynqsiimkxbbjba'
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
        test_value = float(10.961287887309378)
        self.instance.precip_quantity = test_value
        self.assertEqual(self.instance.precip_quantity, test_value)
    
    def test_temp_dry_shelter_avg_property(self):
        """
        Test temp_dry_shelter_avg property
        """
        test_value = float(3.1993786447440775)
        self.instance.temp_dry_shelter_avg = test_value
        self.assertEqual(self.instance.temp_dry_shelter_avg, test_value)
    
    def test_temp_grass_pt100_avg_property(self):
        """
        Test temp_grass_pt100_avg property
        """
        test_value = float(60.55034204459707)
        self.instance.temp_grass_pt100_avg = test_value
        self.assertEqual(self.instance.temp_grass_pt100_avg, test_value)
    
    def test_temp_soil_avg_property(self):
        """
        Test temp_soil_avg property
        """
        test_value = float(47.75924100768082)
        self.instance.temp_soil_avg = test_value
        self.assertEqual(self.instance.temp_soil_avg, test_value)
    
    def test_temp_soil_avg_5cm_property(self):
        """
        Test temp_soil_avg_5cm property
        """
        test_value = float(92.96607799500227)
        self.instance.temp_soil_avg_5cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_5cm, test_value)
    
    def test_temp_soil_avg_10cm_property(self):
        """
        Test temp_soil_avg_10cm property
        """
        test_value = float(0.22598038735198722)
        self.instance.temp_soil_avg_10cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_10cm, test_value)
    
    def test_temp_soil_avg_20cm_property(self):
        """
        Test temp_soil_avg_20cm property
        """
        test_value = float(64.50842024928875)
        self.instance.temp_soil_avg_20cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_20cm, test_value)
    
    def test_temp_soil_avg_50cm_property(self):
        """
        Test temp_soil_avg_50cm property
        """
        test_value = float(74.20229221702492)
        self.instance.temp_soil_avg_50cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_50cm, test_value)
    
    def test_wind_speed_10m_property(self):
        """
        Test wind_speed_10m property
        """
        test_value = float(67.76297452608567)
        self.instance.wind_speed_10m = test_value
        self.assertEqual(self.instance.wind_speed_10m, test_value)
    
    def test_wind_speed_avg_30m_property(self):
        """
        Test wind_speed_avg_30m property
        """
        test_value = float(99.16252700378118)
        self.instance.wind_speed_avg_30m = test_value
        self.assertEqual(self.instance.wind_speed_avg_30m, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(65.38948206643545)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gusts_speed_property(self):
        """
        Test wind_gusts_speed property
        """
        test_value = float(62.40356303135023)
        self.instance.wind_gusts_speed = test_value
        self.assertEqual(self.instance.wind_gusts_speed, test_value)
    
    def test_humidity_rel_shelter_avg_property(self):
        """
        Test humidity_rel_shelter_avg property
        """
        test_value = float(55.29522160490193)
        self.instance.humidity_rel_shelter_avg = test_value
        self.assertEqual(self.instance.humidity_rel_shelter_avg, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(25.939443530480986)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_sun_duration_property(self):
        """
        Test sun_duration property
        """
        test_value = float(36.60873821866857)
        self.instance.sun_duration = test_value
        self.assertEqual(self.instance.sun_duration, test_value)
    
    def test_short_wave_from_sky_avg_property(self):
        """
        Test short_wave_from_sky_avg property
        """
        test_value = float(33.183670556294956)
        self.instance.short_wave_from_sky_avg = test_value
        self.assertEqual(self.instance.short_wave_from_sky_avg, test_value)
    
    def test_sun_int_avg_property(self):
        """
        Test sun_int_avg property
        """
        test_value = float(35.18478090168323)
        self.instance.sun_int_avg = test_value
        self.assertEqual(self.instance.sun_int_avg, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'zstitvmwpwvlklkogwzc'
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

