"""
Test case for SolarWindPlasma
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.solarwindplasma import SolarWindPlasma


class Test_SolarWindPlasma(unittest.TestCase):
    """
    Test case for SolarWindPlasma
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SolarWindPlasma.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SolarWindPlasma for testing
        """
        instance = SolarWindPlasma(
            observation_time='spsrqakiieiriwwifvnf',
            density=float(18.92751786196749),
            speed=float(95.5988763257844),
            temperature=float(37.00980475889721)
        )
        return instance

    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'spsrqakiieiriwwifvnf'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_density_property(self):
        """
        Test density property
        """
        test_value = float(18.92751786196749)
        self.instance.density = test_value
        self.assertEqual(self.instance.density, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(95.5988763257844)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(37.00980475889721)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SolarWindPlasma.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SolarWindPlasma.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

