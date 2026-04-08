"""
Test case for BuoyObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.buoyobservation import BuoyObservation
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
            station_id='zqdujrhlhbgtjwfdbfgm',
            latitude=float(5.948450034646468),
            longitude=float(45.18090951418453),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(0.5571652954654005),
            wind_speed=float(28.0395354286072),
            gust=float(35.253172496823815),
            wave_height=float(28.613625245014298),
            dominant_wave_period=float(45.1503435483181),
            average_wave_period=float(33.88033270874053),
            mean_wave_direction=float(30.652290744290024),
            pressure=float(89.48019815213712),
            air_temperature=float(77.2831567794461),
            water_temperature=float(67.11838931022302),
            dewpoint=float(21.795771015662357),
            pressure_tendency=float(12.813540740154428),
            visibility=float(5.20033525911553),
            tide=float(94.26660153240003)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zqdujrhlhbgtjwfdbfgm'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(5.948450034646468)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(45.18090951418453)
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
        test_value = float(0.5571652954654005)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(28.0395354286072)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(35.253172496823815)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_wave_height_property(self):
        """
        Test wave_height property
        """
        test_value = float(28.613625245014298)
        self.instance.wave_height = test_value
        self.assertEqual(self.instance.wave_height, test_value)
    
    def test_dominant_wave_period_property(self):
        """
        Test dominant_wave_period property
        """
        test_value = float(45.1503435483181)
        self.instance.dominant_wave_period = test_value
        self.assertEqual(self.instance.dominant_wave_period, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(33.88033270874053)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(30.652290744290024)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(89.48019815213712)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(77.2831567794461)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(67.11838931022302)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_dewpoint_property(self):
        """
        Test dewpoint property
        """
        test_value = float(21.795771015662357)
        self.instance.dewpoint = test_value
        self.assertEqual(self.instance.dewpoint, test_value)
    
    def test_pressure_tendency_property(self):
        """
        Test pressure_tendency property
        """
        test_value = float(12.813540740154428)
        self.instance.pressure_tendency = test_value
        self.assertEqual(self.instance.pressure_tendency, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(5.20033525911553)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_tide_property(self):
        """
        Test tide property
        """
        test_value = float(94.26660153240003)
        self.instance.tide = test_value
        self.assertEqual(self.instance.tide, test_value)
    
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

