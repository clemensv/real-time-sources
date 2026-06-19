"""
Test case for WaterLevel
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.waterlevel import WaterLevel
from noaa_producer_data.microsoft.opendata.us.noaa.qualityenum import QualityEnum


class Test_WaterLevel(unittest.TestCase):
    """
    Test case for WaterLevel
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevel.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevel for testing
        """
        instance = WaterLevel(
            station_id='azsffwvrmnhbtwitpmuf',
            timestamp='jrwnagfszeiddxbdvnho',
            value=float(15.26411875437914),
            stddev=float(0.3594346824369876),
            outside_sigma_band=False,
            flat_tolerance_limit=True,
            rate_of_change_limit=True,
            max_min_expected_height=False,
            quality=QualityEnum.Preliminary,
            region='txnpwdzrldnwgdmfascp'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'azsffwvrmnhbtwitpmuf'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'jrwnagfszeiddxbdvnho'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(15.26411875437914)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_stddev_property(self):
        """
        Test stddev property
        """
        test_value = float(0.3594346824369876)
        self.instance.stddev = test_value
        self.assertEqual(self.instance.stddev, test_value)
    
    def test_outside_sigma_band_property(self):
        """
        Test outside_sigma_band property
        """
        test_value = False
        self.instance.outside_sigma_band = test_value
        self.assertEqual(self.instance.outside_sigma_band, test_value)
    
    def test_flat_tolerance_limit_property(self):
        """
        Test flat_tolerance_limit property
        """
        test_value = True
        self.instance.flat_tolerance_limit = test_value
        self.assertEqual(self.instance.flat_tolerance_limit, test_value)
    
    def test_rate_of_change_limit_property(self):
        """
        Test rate_of_change_limit property
        """
        test_value = True
        self.instance.rate_of_change_limit = test_value
        self.assertEqual(self.instance.rate_of_change_limit, test_value)
    
    def test_max_min_expected_height_property(self):
        """
        Test max_min_expected_height property
        """
        test_value = False
        self.instance.max_min_expected_height = test_value
        self.assertEqual(self.instance.max_min_expected_height, test_value)
    
    def test_quality_property(self):
        """
        Test quality property
        """
        test_value = QualityEnum.Preliminary
        self.instance.quality = test_value
        self.assertEqual(self.instance.quality, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'txnpwdzrldnwgdmfascp'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevel.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevel.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

