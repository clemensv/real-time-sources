"""
Test case for SolarWindMagField
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.microsoft.opendata.us.noaa.swpc.solarwindmagfield import SolarWindMagField


class Test_SolarWindMagField(unittest.TestCase):
    """
    Test case for SolarWindMagField
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SolarWindMagField.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SolarWindMagField for testing
        """
        instance = SolarWindMagField(
            observation_time='uwjlmqhhcinhfmlfwrxf',
            bx_gsm=float(2.094439682247118),
            by_gsm=float(2.7633177784601726),
            bz_gsm=float(30.922908107171754),
            lon_gsm=float(75.50289469698286),
            lat_gsm=float(58.58499398192855),
            bt=float(40.766861276468426)
        )
        return instance

    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'uwjlmqhhcinhfmlfwrxf'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_bx_gsm_property(self):
        """
        Test bx_gsm property
        """
        test_value = float(2.094439682247118)
        self.instance.bx_gsm = test_value
        self.assertEqual(self.instance.bx_gsm, test_value)
    
    def test_by_gsm_property(self):
        """
        Test by_gsm property
        """
        test_value = float(2.7633177784601726)
        self.instance.by_gsm = test_value
        self.assertEqual(self.instance.by_gsm, test_value)
    
    def test_bz_gsm_property(self):
        """
        Test bz_gsm property
        """
        test_value = float(30.922908107171754)
        self.instance.bz_gsm = test_value
        self.assertEqual(self.instance.bz_gsm, test_value)
    
    def test_lon_gsm_property(self):
        """
        Test lon_gsm property
        """
        test_value = float(75.50289469698286)
        self.instance.lon_gsm = test_value
        self.assertEqual(self.instance.lon_gsm, test_value)
    
    def test_lat_gsm_property(self):
        """
        Test lat_gsm property
        """
        test_value = float(58.58499398192855)
        self.instance.lat_gsm = test_value
        self.assertEqual(self.instance.lat_gsm, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(40.766861276468426)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SolarWindMagField.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
