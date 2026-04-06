"""
Test case for CurrentPredictions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.currentpredictions import CurrentPredictions


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
            station_id='tatjpawgkyqiejeasigy',
            timestamp='enbshsrrrtfruieruokv',
            velocity_major=float(68.28041168528787),
            mean_flood_dir=float(5.91303469970188),
            mean_ebb_dir=float(26.34529059813785),
            depth=float(59.07715473891593),
            bin='jszfhmprsdvrzleymzud'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tatjpawgkyqiejeasigy'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'enbshsrrrtfruieruokv'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_velocity_major_property(self):
        """
        Test velocity_major property
        """
        test_value = float(68.28041168528787)
        self.instance.velocity_major = test_value
        self.assertEqual(self.instance.velocity_major, test_value)
    
    def test_mean_flood_dir_property(self):
        """
        Test mean_flood_dir property
        """
        test_value = float(5.91303469970188)
        self.instance.mean_flood_dir = test_value
        self.assertEqual(self.instance.mean_flood_dir, test_value)
    
    def test_mean_ebb_dir_property(self):
        """
        Test mean_ebb_dir property
        """
        test_value = float(26.34529059813785)
        self.instance.mean_ebb_dir = test_value
        self.assertEqual(self.instance.mean_ebb_dir, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(59.07715473891593)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_bin_property(self):
        """
        Test bin property
        """
        test_value = 'jszfhmprsdvrzleymzud'
        self.instance.bin = test_value
        self.assertEqual(self.instance.bin, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CurrentPredictions.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
