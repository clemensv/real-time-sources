"""
Test case for OfsMapOffsets
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.stationtypes.ofsmapoffsets import OfsMapOffsets


class Test_OfsMapOffsets(unittest.TestCase):
    """
    Test case for OfsMapOffsets
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_OfsMapOffsets.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OfsMapOffsets for testing
        """
        instance = OfsMapOffsets(
            self_='ybnxbcxjhbgpcdbrykgf'
        )
        return instance

    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'ybnxbcxjhbgpcdbrykgf'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = OfsMapOffsets.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
