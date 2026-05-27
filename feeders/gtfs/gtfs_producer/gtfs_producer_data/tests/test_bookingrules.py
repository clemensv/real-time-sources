"""
Test case for BookingRules
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.bookingrules import BookingRules


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
            bookingRuleId='jcchyijxwfadkvnqoebs',
            bookingRuleName='gadjrgwzrlnwxbvdwxwf',
            bookingRuleDesc='qhqtnwfqogzirogvofgs',
            bookingRuleUrl='fbgfswduvbqsazvfksdp'
        )
        return instance

    
    def test_bookingRuleId_property(self):
        """
        Test bookingRuleId property
        """
        test_value = 'jcchyijxwfadkvnqoebs'
        self.instance.bookingRuleId = test_value
        self.assertEqual(self.instance.bookingRuleId, test_value)
    
    def test_bookingRuleName_property(self):
        """
        Test bookingRuleName property
        """
        test_value = 'gadjrgwzrlnwxbvdwxwf'
        self.instance.bookingRuleName = test_value
        self.assertEqual(self.instance.bookingRuleName, test_value)
    
    def test_bookingRuleDesc_property(self):
        """
        Test bookingRuleDesc property
        """
        test_value = 'qhqtnwfqogzirogvofgs'
        self.instance.bookingRuleDesc = test_value
        self.assertEqual(self.instance.bookingRuleDesc, test_value)
    
    def test_bookingRuleUrl_property(self):
        """
        Test bookingRuleUrl property
        """
        test_value = 'fbgfswduvbqsazvfksdp'
        self.instance.bookingRuleUrl = test_value
        self.assertEqual(self.instance.bookingRuleUrl, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BookingRules.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BookingRules.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

