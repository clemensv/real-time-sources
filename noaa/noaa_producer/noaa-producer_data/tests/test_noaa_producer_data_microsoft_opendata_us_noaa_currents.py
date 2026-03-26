"""
Test case for Currents
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.currents import Currents


class Test_Currents(unittest.TestCase):
    """
    Test case for Currents
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Currents.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Currents for testing
        """
        instance = Currents(
            station_id='yfabtfkxbhgyqbmgtczw',
            timestamp='btdqgpjrwkohhghiekoc',
            speed=float(98.7584169108117),
            direction_degrees=float(20.656939496885897),
            bin='ekqseeeuiwrjkwpenwkz'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'yfabtfkxbhgyqbmgtczw'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'btdqgpjrwkohhghiekoc'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(98.7584169108117)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_direction_degrees_property(self):
        """
        Test direction_degrees property
        """
        test_value = float(20.656939496885897)
        self.instance.direction_degrees = test_value
        self.assertEqual(self.instance.direction_degrees, test_value)
    
    def test_bin_property(self):
        """
        Test bin property
        """
        test_value = 'ekqseeeuiwrjkwpenwkz'
        self.instance.bin = test_value
        self.assertEqual(self.instance.bin, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Currents.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
