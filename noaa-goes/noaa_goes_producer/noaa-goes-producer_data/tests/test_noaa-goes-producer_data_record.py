"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa-goes-producer_data.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            time_tag='plmevhcluyibhiamcjri',
            kp=float(96.03837730483721),
            a_running=float(83.63248430850408),
            station_count=float(62.178827456068234)
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'plmevhcluyibhiamcjri'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_kp_property(self):
        """
        Test kp property
        """
        test_value = float(96.03837730483721)
        self.instance.kp = test_value
        self.assertEqual(self.instance.kp, test_value)
    
    def test_a_running_property(self):
        """
        Test a_running property
        """
        test_value = float(83.63248430850408)
        self.instance.a_running = test_value
        self.assertEqual(self.instance.a_running, test_value)
    
    def test_station_count_property(self):
        """
        Test station_count property
        """
        test_value = float(62.178827456068234)
        self.instance.station_count = test_value
        self.assertEqual(self.instance.station_count, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
