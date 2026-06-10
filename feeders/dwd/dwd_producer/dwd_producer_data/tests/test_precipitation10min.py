"""
Test case for Precipitation10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.precipitation10min import Precipitation10Min


class Test_Precipitation10Min(unittest.TestCase):
    """
    Test case for Precipitation10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Precipitation10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Precipitation10Min for testing
        """
        instance = Precipitation10Min(
            station_id='tdbdtnndpbuawiflckep',
            timestamp='knemvwuspafifyzuyofo',
            quality_level=int(47),
            precipitation_height=float(49.949902053921804),
            precipitation_indicator=int(44),
            state='gbfkwnqzjbkagmsdsmie'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tdbdtnndpbuawiflckep'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'knemvwuspafifyzuyofo'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(47)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_precipitation_height_property(self):
        """
        Test precipitation_height property
        """
        test_value = float(49.949902053921804)
        self.instance.precipitation_height = test_value
        self.assertEqual(self.instance.precipitation_height, test_value)
    
    def test_precipitation_indicator_property(self):
        """
        Test precipitation_indicator property
        """
        test_value = int(44)
        self.instance.precipitation_indicator = test_value
        self.assertEqual(self.instance.precipitation_indicator, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'gbfkwnqzjbkagmsdsmie'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Precipitation10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Precipitation10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

