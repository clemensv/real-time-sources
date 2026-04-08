"""
Test case for SolarWindPlasma
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.microsoft.opendata.us.noaa.swpc.solarwindplasma import SolarWindPlasma


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
            observation_time='gidfkbbehbnkfnhlhjgf',
            density=float(99.11196370093998),
            speed=float(4.173128544503735),
            temperature=float(55.26697704123366)
        )
        return instance

    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'gidfkbbehbnkfnhlhjgf'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_density_property(self):
        """
        Test density property
        """
        test_value = float(99.11196370093998)
        self.instance.density = test_value
        self.assertEqual(self.instance.density, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(4.173128544503735)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(55.26697704123366)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SolarWindPlasma.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
