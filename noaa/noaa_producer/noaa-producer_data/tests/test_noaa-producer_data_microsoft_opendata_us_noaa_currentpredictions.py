"""
Test case for CurrentPredictions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa-producer_data.microsoft.opendata.us.noaa.currentpredictions import CurrentPredictions


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
            station_id='qfautbvbluejvwqxfuxr',
            timestamp='frdroohbcifrbtixtmoy',
            velocity_major=float(32.13113045006173),
            mean_flood_dir=float(64.25080464942015),
            mean_ebb_dir=float(71.0881702565733),
            depth=float(74.53693546851562),
            bin='gqdhauffkfmmhtfrapxp'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'qfautbvbluejvwqxfuxr'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'frdroohbcifrbtixtmoy'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_velocity_major_property(self):
        """
        Test velocity_major property
        """
        test_value = float(32.13113045006173)
        self.instance.velocity_major = test_value
        self.assertEqual(self.instance.velocity_major, test_value)
    
    def test_mean_flood_dir_property(self):
        """
        Test mean_flood_dir property
        """
        test_value = float(64.25080464942015)
        self.instance.mean_flood_dir = test_value
        self.assertEqual(self.instance.mean_flood_dir, test_value)
    
    def test_mean_ebb_dir_property(self):
        """
        Test mean_ebb_dir property
        """
        test_value = float(71.0881702565733)
        self.instance.mean_ebb_dir = test_value
        self.assertEqual(self.instance.mean_ebb_dir, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(74.53693546851562)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_bin_property(self):
        """
        Test bin property
        """
        test_value = 'gqdhauffkfmmhtfrapxp'
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
