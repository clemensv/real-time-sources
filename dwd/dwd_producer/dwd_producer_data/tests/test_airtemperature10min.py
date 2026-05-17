"""
Test case for AirTemperature10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.airtemperature10min import AirTemperature10Min


class Test_AirTemperature10Min(unittest.TestCase):
    """
    Test case for AirTemperature10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AirTemperature10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AirTemperature10Min for testing
        """
        instance = AirTemperature10Min(
            station_id='ntbyixnubsdibcwvdqfx',
            timestamp='owsfrvdbxmrmlballumb',
            quality_level=int(48),
            pressure_station_level=float(94.3182310060743),
            air_temperature_2m=float(18.31186906086131),
            air_temperature_5cm=float(33.42922089112258),
            relative_humidity=float(66.21151831298306),
            dew_point_temperature=float(21.028218058975177)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ntbyixnubsdibcwvdqfx'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'owsfrvdbxmrmlballumb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(48)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_pressure_station_level_property(self):
        """
        Test pressure_station_level property
        """
        test_value = float(94.3182310060743)
        self.instance.pressure_station_level = test_value
        self.assertEqual(self.instance.pressure_station_level, test_value)
    
    def test_air_temperature_2m_property(self):
        """
        Test air_temperature_2m property
        """
        test_value = float(18.31186906086131)
        self.instance.air_temperature_2m = test_value
        self.assertEqual(self.instance.air_temperature_2m, test_value)
    
    def test_air_temperature_5cm_property(self):
        """
        Test air_temperature_5cm property
        """
        test_value = float(33.42922089112258)
        self.instance.air_temperature_5cm = test_value
        self.assertEqual(self.instance.air_temperature_5cm, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = float(66.21151831298306)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_dew_point_temperature_property(self):
        """
        Test dew_point_temperature property
        """
        test_value = float(21.028218058975177)
        self.instance.dew_point_temperature = test_value
        self.assertEqual(self.instance.dew_point_temperature, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AirTemperature10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AirTemperature10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

