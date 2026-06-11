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
            station_id='fgdfbiiiyyaspkcbgowy',
            station_name='czsodwmilwjhvsdsskdc',
            reading_time='vuqbgxwhwesyqleerlmx',
            temperature_in_fahrenheit=float(58.74549230334394),
            precipitation_in_inches=float(45.50497682821456),
            wind_speed_in_mph=float(88.59519658820035),
            wind_gust_speed_in_mph=float(86.64791213542901),
            wind_direction=int(50),
            wind_direction_cardinal='ttnxrmecjqubjiwryxyq',
            barometric_pressure=float(2.490840884611545),
            relative_humidity=int(96),
            visibility=float(31.714972846556535),
            sky_coverage='lfyeqejsyzkbrgtfkvlg',
            latitude=float(17.12042874257458),
            longitude=float(19.8197811491617)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fgdfbiiiyyaspkcbgowy'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'czsodwmilwjhvsdsskdc'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = 'vuqbgxwhwesyqleerlmx'
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = float(58.74549230334394)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_precipitation_in_inches_property(self):
        """
        Test precipitation_in_inches property
        """
        test_value = float(45.50497682821456)
        self.instance.precipitation_in_inches = test_value
        self.assertEqual(self.instance.precipitation_in_inches, test_value)
    
    def test_wind_speed_in_mph_property(self):
        """
        Test wind_speed_in_mph property
        """
        test_value = float(88.59519658820035)
        self.instance.wind_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_speed_in_mph, test_value)
    
    def test_wind_gust_speed_in_mph_property(self):
        """
        Test wind_gust_speed_in_mph property
        """
        test_value = float(86.64791213542901)
        self.instance.wind_gust_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_gust_speed_in_mph, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = int(50)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_cardinal_property(self):
        """
        Test wind_direction_cardinal property
        """
        test_value = 'ttnxrmecjqubjiwryxyq'
        self.instance.wind_direction_cardinal = test_value
        self.assertEqual(self.instance.wind_direction_cardinal, test_value)
    
    def test_barometric_pressure_property(self):
        """
        Test barometric_pressure property
        """
        test_value = float(2.490840884611545)
        self.instance.barometric_pressure = test_value
        self.assertEqual(self.instance.barometric_pressure, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(96)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(31.714972846556535)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_sky_coverage_property(self):
        """
        Test sky_coverage property
        """
        test_value = 'lfyeqejsyzkbrgtfkvlg'
        self.instance.sky_coverage = test_value
        self.assertEqual(self.instance.sky_coverage, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(17.12042874257458)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(19.8197811491617)
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

