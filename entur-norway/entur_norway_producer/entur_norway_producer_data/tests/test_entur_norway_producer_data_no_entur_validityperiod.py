"""
Test case for ValidityPeriod
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.validityperiod import ValidityPeriod


class Test_ValidityPeriod(unittest.TestCase):
    """
    Test case for ValidityPeriod
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ValidityPeriod.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ValidityPeriod for testing
        """
        instance = ValidityPeriod(
            start_time='gxgqxtswcfrrywdrlqbc',
            end_time='bpsgyhcpkxfilfzpyasz'
        )
        return instance

    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'gxgqxtswcfrrywdrlqbc'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'bpsgyhcpkxfilfzpyasz'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ValidityPeriod.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
