"""
Test case for Wind10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_amqp_producer_data.wind10min import Wind10Min


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
            station_id='aylvdwhyroujwyxphvbl',
            timestamp='dqxdonmveipsymgutvub',
            quality_level=int(20),
            wind_speed=float(22.6154067284989),
            wind_direction=float(18.864967969563228),
            state='lelnxfmmargphdaoslry'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'aylvdwhyroujwyxphvbl'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'dqxdonmveipsymgutvub'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(20)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(22.6154067284989)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(18.864967969563228)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'lelnxfmmargphdaoslry'
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

