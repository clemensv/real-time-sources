"""
Test case for WeatherReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.weather.weatherreading import WeatherReading


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
            station_id='qrydnpmwltrefcraeubb',
            station_name='fquoqjaxkbtuityhoihn',
            reading_time='cnlrqyzxjgtpwwhwnzgw',
            temperature_in_fahrenheit=float(33.91257833912399),
            precipitation_in_inches=float(29.01804129244282),
            wind_speed_in_mph=float(88.66141601061229),
            wind_gust_speed_in_mph=float(60.265193484903),
            wind_direction=int(41),
            wind_direction_cardinal='tvtzuxcjhkczoetubema',
            barometric_pressure=float(25.256476966803753),
            relative_humidity=int(9),
            visibility=float(17.309011933439344),
            sky_coverage='rkpbqdovbsgcikcnuprl',
            latitude=float(72.1911594054643),
            longitude=float(44.020743583624125)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'qrydnpmwltrefcraeubb'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'fquoqjaxkbtuityhoihn'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = 'cnlrqyzxjgtpwwhwnzgw'
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = float(33.91257833912399)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_precipitation_in_inches_property(self):
        """
        Test precipitation_in_inches property
        """
        test_value = float(29.01804129244282)
        self.instance.precipitation_in_inches = test_value
        self.assertEqual(self.instance.precipitation_in_inches, test_value)
    
    def test_wind_speed_in_mph_property(self):
        """
        Test wind_speed_in_mph property
        """
        test_value = float(88.66141601061229)
        self.instance.wind_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_speed_in_mph, test_value)
    
    def test_wind_gust_speed_in_mph_property(self):
        """
        Test wind_gust_speed_in_mph property
        """
        test_value = float(60.265193484903)
        self.instance.wind_gust_speed_in_mph = test_value
        self.assertEqual(self.instance.wind_gust_speed_in_mph, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = int(41)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_cardinal_property(self):
        """
        Test wind_direction_cardinal property
        """
        test_value = 'tvtzuxcjhkczoetubema'
        self.instance.wind_direction_cardinal = test_value
        self.assertEqual(self.instance.wind_direction_cardinal, test_value)
    
    def test_barometric_pressure_property(self):
        """
        Test barometric_pressure property
        """
        test_value = float(25.256476966803753)
        self.instance.barometric_pressure = test_value
        self.assertEqual(self.instance.barometric_pressure, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(9)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(17.309011933439344)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_sky_coverage_property(self):
        """
        Test sky_coverage property
        """
        test_value = 'rkpbqdovbsgcikcnuprl'
        self.instance.sky_coverage = test_value
        self.assertEqual(self.instance.sky_coverage, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(72.1911594054643)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(44.020743583624125)
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

