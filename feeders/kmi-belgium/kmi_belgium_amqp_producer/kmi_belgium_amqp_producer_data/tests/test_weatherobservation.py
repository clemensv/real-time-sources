"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kmi_belgium_amqp_producer_data.weatherobservation import WeatherObservation
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
            station_code='znixlkjpnecxtzacymdn',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            precip_quantity=float(61.08297459991374),
            temp_dry_shelter_avg=float(87.36875624108457),
            temp_grass_pt100_avg=float(11.717258564615186),
            temp_soil_avg=float(64.95730909103634),
            temp_soil_avg_5cm=float(1.5059855660549126),
            temp_soil_avg_10cm=float(72.12053539200241),
            temp_soil_avg_20cm=float(72.93088301312449),
            temp_soil_avg_50cm=float(76.61635318141808),
            wind_speed_10m=float(78.26639122017117),
            wind_speed_avg_30m=float(67.03317471777035),
            wind_direction=float(57.71176734111607),
            wind_gusts_speed=float(61.42757955077681),
            humidity_rel_shelter_avg=float(9.157050081494333),
            pressure=float(24.003728402628376),
            sun_duration=float(73.73446286661569),
            short_wave_from_sky_avg=float(25.557075170368027),
            sun_int_avg=float(25.494820721767862),
            region='bxbdpcvuazycgayssbgx'
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'znixlkjpnecxtzacymdn'
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
        test_value = float(61.08297459991374)
        self.instance.precip_quantity = test_value
        self.assertEqual(self.instance.precip_quantity, test_value)
    
    def test_temp_dry_shelter_avg_property(self):
        """
        Test temp_dry_shelter_avg property
        """
        test_value = float(87.36875624108457)
        self.instance.temp_dry_shelter_avg = test_value
        self.assertEqual(self.instance.temp_dry_shelter_avg, test_value)
    
    def test_temp_grass_pt100_avg_property(self):
        """
        Test temp_grass_pt100_avg property
        """
        test_value = float(11.717258564615186)
        self.instance.temp_grass_pt100_avg = test_value
        self.assertEqual(self.instance.temp_grass_pt100_avg, test_value)
    
    def test_temp_soil_avg_property(self):
        """
        Test temp_soil_avg property
        """
        test_value = float(64.95730909103634)
        self.instance.temp_soil_avg = test_value
        self.assertEqual(self.instance.temp_soil_avg, test_value)
    
    def test_temp_soil_avg_5cm_property(self):
        """
        Test temp_soil_avg_5cm property
        """
        test_value = float(1.5059855660549126)
        self.instance.temp_soil_avg_5cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_5cm, test_value)
    
    def test_temp_soil_avg_10cm_property(self):
        """
        Test temp_soil_avg_10cm property
        """
        test_value = float(72.12053539200241)
        self.instance.temp_soil_avg_10cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_10cm, test_value)
    
    def test_temp_soil_avg_20cm_property(self):
        """
        Test temp_soil_avg_20cm property
        """
        test_value = float(72.93088301312449)
        self.instance.temp_soil_avg_20cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_20cm, test_value)
    
    def test_temp_soil_avg_50cm_property(self):
        """
        Test temp_soil_avg_50cm property
        """
        test_value = float(76.61635318141808)
        self.instance.temp_soil_avg_50cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_50cm, test_value)
    
    def test_wind_speed_10m_property(self):
        """
        Test wind_speed_10m property
        """
        test_value = float(78.26639122017117)
        self.instance.wind_speed_10m = test_value
        self.assertEqual(self.instance.wind_speed_10m, test_value)
    
    def test_wind_speed_avg_30m_property(self):
        """
        Test wind_speed_avg_30m property
        """
        test_value = float(67.03317471777035)
        self.instance.wind_speed_avg_30m = test_value
        self.assertEqual(self.instance.wind_speed_avg_30m, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(57.71176734111607)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gusts_speed_property(self):
        """
        Test wind_gusts_speed property
        """
        test_value = float(61.42757955077681)
        self.instance.wind_gusts_speed = test_value
        self.assertEqual(self.instance.wind_gusts_speed, test_value)
    
    def test_humidity_rel_shelter_avg_property(self):
        """
        Test humidity_rel_shelter_avg property
        """
        test_value = float(9.157050081494333)
        self.instance.humidity_rel_shelter_avg = test_value
        self.assertEqual(self.instance.humidity_rel_shelter_avg, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(24.003728402628376)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_sun_duration_property(self):
        """
        Test sun_duration property
        """
        test_value = float(73.73446286661569)
        self.instance.sun_duration = test_value
        self.assertEqual(self.instance.sun_duration, test_value)
    
    def test_short_wave_from_sky_avg_property(self):
        """
        Test short_wave_from_sky_avg property
        """
        test_value = float(25.557075170368027)
        self.instance.short_wave_from_sky_avg = test_value
        self.assertEqual(self.instance.short_wave_from_sky_avg, test_value)
    
    def test_sun_int_avg_property(self):
        """
        Test sun_int_avg property
        """
        test_value = float(25.494820721767862)
        self.instance.sun_int_avg = test_value
        self.assertEqual(self.instance.sun_int_avg, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'bxbdpcvuazycgayssbgx'
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

