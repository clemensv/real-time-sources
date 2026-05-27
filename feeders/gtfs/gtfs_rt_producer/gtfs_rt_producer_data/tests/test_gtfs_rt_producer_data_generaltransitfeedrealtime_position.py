"""
Test case for Position
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.position import Position

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
            latitude=float(59.940333298038595),
            longitude=float(3.966636425512904),
            bearing=float(73.37334651523261),
            odometer=float(15.296499566204314),
            speed=float(49.659457537356786)
        )
        return instance

    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(59.940333298038595)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(3.966636425512904)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = float(73.37334651523261)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_odometer_property(self):
        """
        Test odometer property
        """
        test_value = float(15.296499566204314)
        self.instance.odometer = test_value
        self.assertEqual(self.instance.odometer, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(49.659457537356786)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
