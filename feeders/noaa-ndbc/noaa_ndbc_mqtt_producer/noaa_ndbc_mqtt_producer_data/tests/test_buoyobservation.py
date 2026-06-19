"""
Test case for BuoyObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_mqtt_producer_data.buoyobservation import BuoyObservation
import datetime


class Test_BuoyObservation(unittest.TestCase):
    """
    Test case for BuoyObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyObservation for testing
        """
        instance = BuoyObservation(
            station_id='vxumrqahgilokjysvpes',
            latitude=float(38.262822177562406),
            longitude=float(41.97631389322034),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(86.09647732068318),
            wind_speed=float(95.96576214472924),
            gust=float(69.89725480367012),
            wave_height=float(70.3545703295257),
            dominant_wave_period=float(88.13780112883268),
            average_wave_period=float(58.807339871725176),
            mean_wave_direction=float(12.181548859392421),
            pressure=float(72.39786104627433),
            air_temperature=float(22.668737134686346),
            water_temperature=float(24.871833159929025),
            dewpoint=float(58.85277821898225),
            pressure_tendency=float(58.85184426843628),
            visibility=float(66.37062557739873),
            tide=float(2.8163731797273495),
            region='isayqvbwceqhxrfcwnls'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vxumrqahgilokjysvpes'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(38.262822177562406)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(41.97631389322034)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(86.09647732068318)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(95.96576214472924)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(69.89725480367012)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_wave_height_property(self):
        """
        Test wave_height property
        """
        test_value = float(70.3545703295257)
        self.instance.wave_height = test_value
        self.assertEqual(self.instance.wave_height, test_value)
    
    def test_dominant_wave_period_property(self):
        """
        Test dominant_wave_period property
        """
        test_value = float(88.13780112883268)
        self.instance.dominant_wave_period = test_value
        self.assertEqual(self.instance.dominant_wave_period, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(58.807339871725176)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(12.181548859392421)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(72.39786104627433)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(22.668737134686346)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(24.871833159929025)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_dewpoint_property(self):
        """
        Test dewpoint property
        """
        test_value = float(58.85277821898225)
        self.instance.dewpoint = test_value
        self.assertEqual(self.instance.dewpoint, test_value)
    
    def test_pressure_tendency_property(self):
        """
        Test pressure_tendency property
        """
        test_value = float(58.85184426843628)
        self.instance.pressure_tendency = test_value
        self.assertEqual(self.instance.pressure_tendency, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(66.37062557739873)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_tide_property(self):
        """
        Test tide property
        """
        test_value = float(2.8163731797273495)
        self.instance.tide = test_value
        self.assertEqual(self.instance.tide, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'isayqvbwceqhxrfcwnls'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoyObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

