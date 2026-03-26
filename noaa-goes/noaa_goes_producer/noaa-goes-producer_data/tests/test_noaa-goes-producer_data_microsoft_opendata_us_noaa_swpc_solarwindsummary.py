"""
Test case for SolarWindSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa-goes-producer_data.microsoft.opendata.us.noaa.swpc.solarwindsummary import SolarWindSummary


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
            timestamp='guojynfvgxlnhmnwtzyd',
            wind_speed=float(6.477712621546972),
            bt=float(93.24476497467053),
            bz=float(55.017159518306556)
        )
        return instance

    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'guojynfvgxlnhmnwtzyd'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(6.477712621546972)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(93.24476497467053)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_bz_property(self):
        """
        Test bz property
        """
        test_value = float(55.017159518306556)
        self.instance.bz = test_value
        self.assertEqual(self.instance.bz, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SolarWindSummary.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
