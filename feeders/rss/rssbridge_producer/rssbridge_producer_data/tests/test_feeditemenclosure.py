"""
Test case for FeedItemEnclosure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemenclosure import FeedItemEnclosure


class Test_FeedItemEnclosure(unittest.TestCase):
    """
    Test case for FeedItemEnclosure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItemEnclosure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItemEnclosure for testing
        """
        instance = FeedItemEnclosure(
            href='ahenbcjwhanumoiqyqpj',
            length=int(30),
            type='rcijxfwvccvtotpoopsi'
        )
        return instance

    
    def test_href_property(self):
        """
        Test href property
        """
        test_value = 'ahenbcjwhanumoiqyqpj'
        self.instance.href = test_value
        self.assertEqual(self.instance.href, test_value)
    
    def test_length_property(self):
        """
        Test length property
        """
        test_value = int(30)
        self.instance.length = test_value
        self.assertEqual(self.instance.length, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'rcijxfwvccvtotpoopsi'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FeedItemEnclosure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FeedItemEnclosure.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

