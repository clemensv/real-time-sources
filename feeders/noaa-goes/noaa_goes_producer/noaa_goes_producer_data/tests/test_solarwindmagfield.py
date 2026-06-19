"""
Test case for SolarWindMagField
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.solarwindmagfield import SolarWindMagField


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
            observation_time='zgqbarwvfvaxhbwxipst',
            bx_gsm=float(19.454230867782663),
            by_gsm=float(93.48075234142951),
            bz_gsm=float(94.55336244619416),
            lon_gsm=float(25.752351002155237),
            lat_gsm=float(54.56591725799148),
            bt=float(25.65952804860737)
        )
        return instance

    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'zgqbarwvfvaxhbwxipst'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_bx_gsm_property(self):
        """
        Test bx_gsm property
        """
        test_value = float(19.454230867782663)
        self.instance.bx_gsm = test_value
        self.assertEqual(self.instance.bx_gsm, test_value)
    
    def test_by_gsm_property(self):
        """
        Test by_gsm property
        """
        test_value = float(93.48075234142951)
        self.instance.by_gsm = test_value
        self.assertEqual(self.instance.by_gsm, test_value)
    
    def test_bz_gsm_property(self):
        """
        Test bz_gsm property
        """
        test_value = float(94.55336244619416)
        self.instance.bz_gsm = test_value
        self.assertEqual(self.instance.bz_gsm, test_value)
    
    def test_lon_gsm_property(self):
        """
        Test lon_gsm property
        """
        test_value = float(25.752351002155237)
        self.instance.lon_gsm = test_value
        self.assertEqual(self.instance.lon_gsm, test_value)
    
    def test_lat_gsm_property(self):
        """
        Test lat_gsm property
        """
        test_value = float(54.56591725799148)
        self.instance.lat_gsm = test_value
        self.assertEqual(self.instance.lat_gsm, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(25.65952804860737)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SolarWindMagField.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SolarWindMagField.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

