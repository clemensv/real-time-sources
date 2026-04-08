"""
Test case for SolarWindSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.solarwindsummary import SolarWindSummary


class Test_SolarWindSummary(unittest.TestCase):
    """
    Test case for SolarWindSummary
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SolarWindSummary.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SolarWindSummary for testing
        """
        instance = SolarWindSummary(
            observation_time='pfqchoewgnhdpglfbknc',
            wind_speed=float(95.7789761965802),
            bt=float(68.0535328022799),
            bz=float(68.5113349818811)
        )
        return instance

    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'pfqchoewgnhdpglfbknc'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(95.7789761965802)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(68.0535328022799)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_bz_property(self):
        """
        Test bz property
        """
        test_value = float(68.5113349818811)
        self.instance.bz = test_value
        self.assertEqual(self.instance.bz, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SolarWindSummary.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SolarWindSummary.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

