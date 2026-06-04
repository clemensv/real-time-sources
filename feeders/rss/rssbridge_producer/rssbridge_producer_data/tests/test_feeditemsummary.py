"""
Test case for FeedItemSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsummary import FeedItemSummary


class Test_FeedItemSummary(unittest.TestCase):
    """
    Test case for FeedItemSummary
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItemSummary.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItemSummary for testing
        """
        instance = FeedItemSummary(
            value='rncgacmdclbcthqnrflu',
            type='ygdmwulrkxuuusfeakra',
            language='soofauvhpkjkoeusuiuu',
            base='mhqhbvgjbnkctxuoydcz'
        )
        return instance

    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = 'rncgacmdclbcthqnrflu'
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'ygdmwulrkxuuusfeakra'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'soofauvhpkjkoeusuiuu'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_base_property(self):
        """
        Test base property
        """
        test_value = 'mhqhbvgjbnkctxuoydcz'
        self.instance.base = test_value
        self.assertEqual(self.instance.base, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FeedItemSummary.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FeedItemSummary.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

