"""
Test case for CurrentPredictions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_amqp_producer_data.microsoft.opendata.us.noaa.currentpredictions import CurrentPredictions


class Test_CurrentPredictions(unittest.TestCase):
    """
    Test case for CurrentPredictions
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CurrentPredictions.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CurrentPredictions for testing
        """
        instance = CurrentPredictions(
            station_id='piycnfjaczmclsbnrsgn',
            timestamp='tooppiwkykuootmqflsw',
            velocity_major=float(91.62740737063938),
            mean_flood_dir=float(79.36897173176712),
            mean_ebb_dir=float(6.2493775323744005),
            depth=float(29.060873475365856),
            bin='cnkbxdmfkjfjshkelcce',
            region='jgoxiyvbywhnlihqqzmw'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'piycnfjaczmclsbnrsgn'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'tooppiwkykuootmqflsw'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_velocity_major_property(self):
        """
        Test velocity_major property
        """
        test_value = float(91.62740737063938)
        self.instance.velocity_major = test_value
        self.assertEqual(self.instance.velocity_major, test_value)
    
    def test_mean_flood_dir_property(self):
        """
        Test mean_flood_dir property
        """
        test_value = float(79.36897173176712)
        self.instance.mean_flood_dir = test_value
        self.assertEqual(self.instance.mean_flood_dir, test_value)
    
    def test_mean_ebb_dir_property(self):
        """
        Test mean_ebb_dir property
        """
        test_value = float(6.2493775323744005)
        self.instance.mean_ebb_dir = test_value
        self.assertEqual(self.instance.mean_ebb_dir, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(29.060873475365856)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_bin_property(self):
        """
        Test bin property
        """
        test_value = 'cnkbxdmfkjfjshkelcce'
        self.instance.bin = test_value
        self.assertEqual(self.instance.bin, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'jgoxiyvbywhnlihqqzmw'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CurrentPredictions.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CurrentPredictions.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

