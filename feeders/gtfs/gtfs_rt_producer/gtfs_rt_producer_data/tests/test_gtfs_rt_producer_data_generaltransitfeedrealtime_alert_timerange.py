"""
Test case for TimeRange
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.timerange import TimeRange


class Test_TimeRange(unittest.TestCase):
    """
    Test case for TimeRange
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TimeRange.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TimeRange for testing
        """
        instance = TimeRange(
            start=int(27),
            end=int(36)
        )
        return instance

    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = int(27)
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = int(36)
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TimeRange.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
