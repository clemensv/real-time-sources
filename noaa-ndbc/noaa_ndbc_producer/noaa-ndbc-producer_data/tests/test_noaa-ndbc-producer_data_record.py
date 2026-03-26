"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa-ndbc-producer_data.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            station_id='tgylvlcetbfccedyvlel',
            latitude=float(97.27382533318647),
            longitude=float(37.246659425541864),
            timestamp='ltvmgizrymjapoaiuhuw',
            wind_direction=float(79.8071509151137),
            wind_speed=float(85.456968904444),
            gust=float(65.41970477504631),
            wave_height=float(95.40810279411768),
            dominant_wave_period=float(91.33840888706905),
            average_wave_period=float(60.93167401857386),
            mean_wave_direction=float(80.81120226356579),
            pressure=float(31.28397575281593),
            air_temperature=float(74.64565334398407),
            water_temperature=float(68.41838432807029),
            dewpoint=float(43.66539660920896)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tgylvlcetbfccedyvlel'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(97.27382533318647)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(37.246659425541864)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'ltvmgizrymjapoaiuhuw'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(79.8071509151137)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(85.456968904444)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(65.41970477504631)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_wave_height_property(self):
        """
        Test wave_height property
        """
        test_value = float(95.40810279411768)
        self.instance.wave_height = test_value
        self.assertEqual(self.instance.wave_height, test_value)
    
    def test_dominant_wave_period_property(self):
        """
        Test dominant_wave_period property
        """
        test_value = float(91.33840888706905)
        self.instance.dominant_wave_period = test_value
        self.assertEqual(self.instance.dominant_wave_period, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(60.93167401857386)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(80.81120226356579)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(31.28397575281593)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(74.64565334398407)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(68.41838432807029)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_dewpoint_property(self):
        """
        Test dewpoint property
        """
        test_value = float(43.66539660920896)
        self.instance.dewpoint = test_value
        self.assertEqual(self.instance.dewpoint, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
