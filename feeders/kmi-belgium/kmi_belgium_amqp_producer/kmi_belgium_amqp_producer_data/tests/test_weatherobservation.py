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
            station_code='cvydkhacryayperuxuwh',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            precip_quantity=float(35.68285787338961),
            temp_dry_shelter_avg=float(63.89207844948036),
            temp_grass_pt100_avg=float(60.51326482451592),
            temp_soil_avg=float(0.6738602770033242),
            temp_soil_avg_5cm=float(80.52348369183446),
            temp_soil_avg_10cm=float(66.6760341794662),
            temp_soil_avg_20cm=float(37.49375254599118),
            temp_soil_avg_50cm=float(47.97090955162303),
            wind_speed_10m=float(12.660959361537794),
            wind_speed_avg_30m=float(20.29214687153622),
            wind_direction=float(59.23494445850744),
            wind_gusts_speed=float(28.22994855179939),
            humidity_rel_shelter_avg=float(67.98238410709943),
            pressure=float(67.36873105744074),
            sun_duration=float(51.61202376869443),
            short_wave_from_sky_avg=float(48.949418189655105),
            sun_int_avg=float(70.96067529622438),
            region='zlhxdztolenbphdugqmd'
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'cvydkhacryayperuxuwh'
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
        test_value = float(35.68285787338961)
        self.instance.precip_quantity = test_value
        self.assertEqual(self.instance.precip_quantity, test_value)
    
    def test_temp_dry_shelter_avg_property(self):
        """
        Test temp_dry_shelter_avg property
        """
        test_value = float(63.89207844948036)
        self.instance.temp_dry_shelter_avg = test_value
        self.assertEqual(self.instance.temp_dry_shelter_avg, test_value)
    
    def test_temp_grass_pt100_avg_property(self):
        """
        Test temp_grass_pt100_avg property
        """
        test_value = float(60.51326482451592)
        self.instance.temp_grass_pt100_avg = test_value
        self.assertEqual(self.instance.temp_grass_pt100_avg, test_value)
    
    def test_temp_soil_avg_property(self):
        """
        Test temp_soil_avg property
        """
        test_value = float(0.6738602770033242)
        self.instance.temp_soil_avg = test_value
        self.assertEqual(self.instance.temp_soil_avg, test_value)
    
    def test_temp_soil_avg_5cm_property(self):
        """
        Test temp_soil_avg_5cm property
        """
        test_value = float(80.52348369183446)
        self.instance.temp_soil_avg_5cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_5cm, test_value)
    
    def test_temp_soil_avg_10cm_property(self):
        """
        Test temp_soil_avg_10cm property
        """
        test_value = float(66.6760341794662)
        self.instance.temp_soil_avg_10cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_10cm, test_value)
    
    def test_temp_soil_avg_20cm_property(self):
        """
        Test temp_soil_avg_20cm property
        """
        test_value = float(37.49375254599118)
        self.instance.temp_soil_avg_20cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_20cm, test_value)
    
    def test_temp_soil_avg_50cm_property(self):
        """
        Test temp_soil_avg_50cm property
        """
        test_value = float(47.97090955162303)
        self.instance.temp_soil_avg_50cm = test_value
        self.assertEqual(self.instance.temp_soil_avg_50cm, test_value)
    
    def test_wind_speed_10m_property(self):
        """
        Test wind_speed_10m property
        """
        test_value = float(12.660959361537794)
        self.instance.wind_speed_10m = test_value
        self.assertEqual(self.instance.wind_speed_10m, test_value)
    
    def test_wind_speed_avg_30m_property(self):
        """
        Test wind_speed_avg_30m property
        """
        test_value = float(20.29214687153622)
        self.instance.wind_speed_avg_30m = test_value
        self.assertEqual(self.instance.wind_speed_avg_30m, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(59.23494445850744)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_gusts_speed_property(self):
        """
        Test wind_gusts_speed property
        """
        test_value = float(28.22994855179939)
        self.instance.wind_gusts_speed = test_value
        self.assertEqual(self.instance.wind_gusts_speed, test_value)
    
    def test_humidity_rel_shelter_avg_property(self):
        """
        Test humidity_rel_shelter_avg property
        """
        test_value = float(67.98238410709943)
        self.instance.humidity_rel_shelter_avg = test_value
        self.assertEqual(self.instance.humidity_rel_shelter_avg, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(67.36873105744074)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_sun_duration_property(self):
        """
        Test sun_duration property
        """
        test_value = float(51.61202376869443)
        self.instance.sun_duration = test_value
        self.assertEqual(self.instance.sun_duration, test_value)
    
    def test_short_wave_from_sky_avg_property(self):
        """
        Test short_wave_from_sky_avg property
        """
        test_value = float(48.949418189655105)
        self.instance.short_wave_from_sky_avg = test_value
        self.assertEqual(self.instance.short_wave_from_sky_avg, test_value)
    
    def test_sun_int_avg_property(self):
        """
        Test sun_int_avg property
        """
        test_value = float(70.96067529622438)
        self.instance.sun_int_avg = test_value
        self.assertEqual(self.instance.sun_int_avg, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'zlhxdztolenbphdugqmd'
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

