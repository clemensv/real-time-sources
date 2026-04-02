"""
Test case for SolarWindSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.microsoft.opendata.us.noaa.swpc.solarwindsummary import SolarWindSummary


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
            timestamp='gpucnflugjfnqsdmrdpc',
            wind_speed=float(2.0052247471248896),
            bt=float(86.66676063727716),
            bz=float(62.923226688117154)
        )
        return instance

    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'gpucnflugjfnqsdmrdpc'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(2.0052247471248896)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(86.66676063727716)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_bz_property(self):
        """
        Test bz property
        """
        test_value = float(62.923226688117154)
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
