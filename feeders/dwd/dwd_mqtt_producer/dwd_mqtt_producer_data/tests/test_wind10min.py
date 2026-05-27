"""
Test case for Wind10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_mqtt_producer_data.wind10min import Wind10Min


class Test_Wind10Min(unittest.TestCase):
    """
    Test case for Wind10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Wind10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Wind10Min for testing
        """
        instance = Wind10Min(
            station_id='zrqnevdlvysixjbpzvfa',
            timestamp='qtjligydidapgujizukn',
            quality_level=int(72),
            wind_speed=float(56.07149572679021),
            wind_direction=float(71.63100910062039),
            state='yrovbluwdlquppmqvhej'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zrqnevdlvysixjbpzvfa'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'qtjligydidapgujizukn'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(72)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(56.07149572679021)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(71.63100910062039)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'yrovbluwdlquppmqvhej'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Wind10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Wind10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

