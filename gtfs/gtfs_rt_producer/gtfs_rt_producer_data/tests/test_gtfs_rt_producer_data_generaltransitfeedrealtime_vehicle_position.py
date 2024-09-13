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
            latitude=float(43.03965021290727),
            longitude=float(30.719461524019632),
            bearing=float(14.864462151321977),
            odometer=float(88.61583780845518),
            speed=float(21.687112898916983)
        )
        return instance

    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(43.03965021290727)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(30.719461524019632)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = float(14.864462151321977)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_odometer_property(self):
        """
        Test odometer property
        """
        test_value = float(88.61583780845518)
        self.instance.odometer = test_value
        self.assertEqual(self.instance.odometer, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(21.687112898916983)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
