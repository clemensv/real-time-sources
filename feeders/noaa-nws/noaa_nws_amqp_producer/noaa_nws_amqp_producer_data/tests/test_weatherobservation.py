"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_amqp_producer_data.weatherobservation import WeatherObservation
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
            station_id='tngehugcdteijzubvtkc',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            text_description='pjtpmhuzjjfmjvjpggcz',
            temperature=float(86.63206545032435),
            dewpoint=float(69.06393631027655),
            wind_direction=float(3.060709458651356),
            wind_speed=float(88.804376069682),
            wind_gust=float(88.83551212695504),
            barometric_pressure=float(51.646383209127656),
            sea_level_pressure=float(21.133680641366237),
            visibility=float(37.82021186193967),
            relative_humidity=float(35.738429644557044),
            wind_chill=float(53.83060975387169),
            heat_index=float(60.48107711862591),
            state='oepljjxvxwfygzmcikpt',
            zone_id='xtaqldtlmznrvhbcwikg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tngehugcdteijzubvtkc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_text_description_property(self):
        """
        Test text_description property
        """
        test_value = 'pjtpmhuzjjfmjvjpggcz'
        self.instance.text_description = test_value
        self.assertEqual(self.instance.text_description, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(86.63206545032435)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_dewpoint_property(self):
        """
        Test dewpoint property
        """
        test_value = float(69.06393631027655)
        self.instance.dewpoint = test_value
        self.assertEqual(self.instance.dewpoint, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(3.060709458651356)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(88.804376069682)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(88.83551212695504)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_barometric_pressure_property(self):
        """
        Test barometric_pressure property
        """
        test_value = float(51.646383209127656)
        self.instance.barometric_pressure = test_value
        self.assertEqual(self.instance.barometric_pressure, test_value)
    
    def test_sea_level_pressure_property(self):
        """
        Test sea_level_pressure property
        """
        test_value = float(21.133680641366237)
        self.instance.sea_level_pressure = test_value
        self.assertEqual(self.instance.sea_level_pressure, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(37.82021186193967)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = float(35.738429644557044)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_wind_chill_property(self):
        """
        Test wind_chill property
        """
        test_value = float(53.83060975387169)
        self.instance.wind_chill = test_value
        self.assertEqual(self.instance.wind_chill, test_value)
    
    def test_heat_index_property(self):
        """
        Test heat_index property
        """
        test_value = float(60.48107711862591)
        self.instance.heat_index = test_value
        self.assertEqual(self.instance.heat_index, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'oepljjxvxwfygzmcikpt'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'xtaqldtlmznrvhbcwikg'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
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

