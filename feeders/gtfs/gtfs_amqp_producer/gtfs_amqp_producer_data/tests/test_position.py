"""
Test case for Position
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.vehicle.position import Position


class Test_Position(unittest.TestCase):
    """
    Test case for Position
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Position.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Position for testing
        """
        instance = Position(
            latitude=float(95.79474789861865),
            longitude=float(92.87313196677715),
            bearing=float(38.98327536258829),
            odometer=float(4.96482159313546),
            speed=float(66.90604858581486)
        )
        return instance

    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(95.79474789861865)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(92.87313196677715)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = float(38.98327536258829)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_odometer_property(self):
        """
        Test odometer property
        """
        test_value = float(4.96482159313546)
        self.instance.odometer = test_value
        self.assertEqual(self.instance.odometer, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(66.90604858581486)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Position.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Position.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

