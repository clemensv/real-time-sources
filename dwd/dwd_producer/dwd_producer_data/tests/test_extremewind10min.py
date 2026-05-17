"""
Test case for ExtremeWind10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.extremewind10min import ExtremeWind10Min


class Test_ExtremeWind10Min(unittest.TestCase):
    """
    Test case for ExtremeWind10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ExtremeWind10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ExtremeWind10Min for testing
        """
        instance = ExtremeWind10Min(
            station_id='kvwkhkuswtahgtosnobx',
            timestamp='krppgabdyrjjxmeccvbk',
            quality_level=int(44),
            wind_speed_maximum=float(8.025964027576027),
            wind_speed_minimum=float(49.01942538922519),
            wind_direction_at_maximum=float(37.42701159328053)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'kvwkhkuswtahgtosnobx'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'krppgabdyrjjxmeccvbk'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(44)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_wind_speed_maximum_property(self):
        """
        Test wind_speed_maximum property
        """
        test_value = float(8.025964027576027)
        self.instance.wind_speed_maximum = test_value
        self.assertEqual(self.instance.wind_speed_maximum, test_value)
    
    def test_wind_speed_minimum_property(self):
        """
        Test wind_speed_minimum property
        """
        test_value = float(49.01942538922519)
        self.instance.wind_speed_minimum = test_value
        self.assertEqual(self.instance.wind_speed_minimum, test_value)
    
    def test_wind_direction_at_maximum_property(self):
        """
        Test wind_direction_at_maximum property
        """
        test_value = float(37.42701159328053)
        self.instance.wind_direction_at_maximum = test_value
        self.assertEqual(self.instance.wind_direction_at_maximum, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ExtremeWind10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ExtremeWind10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

