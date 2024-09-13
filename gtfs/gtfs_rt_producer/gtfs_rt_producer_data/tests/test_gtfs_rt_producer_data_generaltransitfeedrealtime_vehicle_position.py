"""
Test case for Position
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.position import Position

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
            latitude=float(7.0838607594650105),
            longitude=float(36.21082371293136),
            bearing=float(8.494893676241698),
            odometer=float(90.8944664713718),
            speed=float(80.84625107105332)
        )
        return instance

    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(7.0838607594650105)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(36.21082371293136)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = float(8.494893676241698)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_odometer_property(self):
        """
        Test odometer property
        """
        test_value = float(90.8944664713718)
        self.instance.odometer = test_value
        self.assertEqual(self.instance.odometer, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(80.84625107105332)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
