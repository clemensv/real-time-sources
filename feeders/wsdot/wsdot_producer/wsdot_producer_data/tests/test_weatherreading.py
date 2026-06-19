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
            station_id='qcpijxiideyzkpkulkyo',
            station_name='fbhnbjyqnielxnvlhfqo',
            reading_time='yqfngpgxxngxdgzxyvlp',
            temperature_in_fahrenheit=float(49.442586572080735),
            precipitation_in_inches=float(31.821410276277675),
            wind_speed_in_mph=float(4.605553824386),
            wind_gust_speed_in_mph=float(64.02176790060321),
            wind_direction=int(59),
            wind_direction_cardinal='jjjmlykpfsbsspsmpffp',
            barometric_pressure=float(1.5878962125316365),
            relative_humidity=int(40),
            visibility=float(64.28915578233317),
            sky_coverage='zjxizjfprdmhkowasule',
            latitude=float(56.64178322010704),
            longitude=float(50.81235223289835)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'qcpijxiideyzkpkulkyo'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'fbhnbjyqnielxnvlhfqo'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = 'yqfngpgxxngxdgzxyvlp'
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = float(49.442586572080735)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_precipitation_in_inches_property(self):
        """
        Test precipitation_in_inches property
        """
        test_value = float(31.821410276277675)
        self.instance.precipitation_in_inches = test_value
        self.assertEqual(self.instance.precipitation_in_inches, test_value)
    
    def test_wind_speed_in_mph_property(self):
        """
        Test wind_speed_in_mph property
        """
        test_value = float(4.605553824386)
        self.instance.wind_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_speed_in_mph, test_value)
    
    def test_wind_gust_speed_in_mph_property(self):
        """
        Test wind_gust_speed_in_mph property
        """
        test_value = float(64.02176790060321)
        self.instance.wind_gust_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_gust_speed_in_mph, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = int(59)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_cardinal_property(self):
        """
        Test wind_direction_cardinal property
        """
        test_value = 'jjjmlykpfsbsspsmpffp'
        self.instance.wind_direction_cardinal = test_value
        self.assertEqual(self.instance.wind_direction_cardinal, test_value)
    
    def test_barometric_pressure_property(self):
        """
        Test barometric_pressure property
        """
        test_value = float(1.5878962125316365)
        self.instance.barometric_pressure = test_value
        self.assertEqual(self.instance.barometric_pressure, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(40)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(64.28915578233317)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_sky_coverage_property(self):
        """
        Test sky_coverage property
        """
        test_value = 'zjxizjfprdmhkowasule'
        self.instance.sky_coverage = test_value
        self.assertEqual(self.instance.sky_coverage, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(56.64178322010704)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(50.81235223289835)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

