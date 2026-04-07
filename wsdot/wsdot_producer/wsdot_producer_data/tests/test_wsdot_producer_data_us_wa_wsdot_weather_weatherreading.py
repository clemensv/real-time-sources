"""
Test case for WeatherReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.weather.weatherreading import WeatherReading


class Test_WeatherReading(unittest.TestCase):
    """
    Test case for WeatherReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherReading for testing
        """
        instance = WeatherReading(
            station_id='pqacmcrcgcdhhurcxsqj',
            station_name='vwxdjalrtaxqlsecgrct',
            reading_time='hzrekooddffxrbzaipnn',
            temperature_in_fahrenheit=float(98.15904178452331),
            precipitation_in_inches=float(52.22386356897795),
            wind_speed_in_mph=float(37.07951461872313),
            wind_gust_speed_in_mph=float(88.24046351475457),
            wind_direction=int(78),
            wind_direction_cardinal='dogfpblecxhonwcpkwpl',
            barometric_pressure=float(32.276859797756806),
            relative_humidity=int(93),
            visibility=float(5.358889456526228),
            sky_coverage='swdtukhwalguiowmdyio',
            latitude=float(14.99203462209131),
            longitude=float(35.18193140350008)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'pqacmcrcgcdhhurcxsqj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'vwxdjalrtaxqlsecgrct'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = 'hzrekooddffxrbzaipnn'
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = float(98.15904178452331)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_precipitation_in_inches_property(self):
        """
        Test precipitation_in_inches property
        """
        test_value = float(52.22386356897795)
        self.instance.precipitation_in_inches = test_value
        self.assertEqual(self.instance.precipitation_in_inches, test_value)
    
    def test_wind_speed_in_mph_property(self):
        """
        Test wind_speed_in_mph property
        """
        test_value = float(37.07951461872313)
        self.instance.wind_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_speed_in_mph, test_value)
    
    def test_wind_gust_speed_in_mph_property(self):
        """
        Test wind_gust_speed_in_mph property
        """
        test_value = float(88.24046351475457)
        self.instance.wind_gust_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_gust_speed_in_mph, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = int(78)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_cardinal_property(self):
        """
        Test wind_direction_cardinal property
        """
        test_value = 'dogfpblecxhonwcpkwpl'
        self.instance.wind_direction_cardinal = test_value
        self.assertEqual(self.instance.wind_direction_cardinal, test_value)
    
    def test_barometric_pressure_property(self):
        """
        Test barometric_pressure property
        """
        test_value = float(32.276859797756806)
        self.instance.barometric_pressure = test_value
        self.assertEqual(self.instance.barometric_pressure, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(93)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(5.358889456526228)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_sky_coverage_property(self):
        """
        Test sky_coverage property
        """
        test_value = 'swdtukhwalguiowmdyio'
        self.instance.sky_coverage = test_value
        self.assertEqual(self.instance.sky_coverage, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(14.99203462209131)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(35.18193140350008)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
