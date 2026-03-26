"""
Test case for BookingRules
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.bookingrules import BookingRules


class Test_BookingRules(unittest.TestCase):
    """
    Test case for BookingRules
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BookingRules.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BookingRules for testing
        """
        instance = BookingRules(
            bookingRuleId='bvshbbtaiqvvhnwyniwy',
            bookingRuleName='lssjjutwccgxlifdmwqb',
            bookingRuleDesc='mtkbyjrgxsoalhvixyyx',
            bookingRuleUrl='ggpxarngofqhkmafkhde'
        )
        return instance

    
    def test_bookingRuleId_property(self):
        """
        Test bookingRuleId property
        """
        test_value = 'bvshbbtaiqvvhnwyniwy'
        self.instance.bookingRuleId = test_value
        self.assertEqual(self.instance.bookingRuleId, test_value)
    
    def test_bookingRuleName_property(self):
        """
        Test bookingRuleName property
        """
        test_value = 'lssjjutwccgxlifdmwqb'
        self.instance.bookingRuleName = test_value
        self.assertEqual(self.instance.bookingRuleName, test_value)
    
    def test_bookingRuleDesc_property(self):
        """
        Test bookingRuleDesc property
        """
        test_value = 'mtkbyjrgxsoalhvixyyx'
        self.instance.bookingRuleDesc = test_value
        self.assertEqual(self.instance.bookingRuleDesc, test_value)
    
    def test_bookingRuleUrl_property(self):
        """
        Test bookingRuleUrl property
        """
        test_value = 'ggpxarngofqhkmafkhde'
        self.instance.bookingRuleUrl = test_value
        self.assertEqual(self.instance.bookingRuleUrl, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BookingRules.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
