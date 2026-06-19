"""
Test case for Link
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link


class Test_Link(unittest.TestCase):
    """
    Test case for Link
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Link.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Link for testing
        """
        instance = Link(
            rel='etsudihnlueoyrysabbq',
            href='vzlnblswiixzrpmkbxte',
            type='fxcsjfozrfjxwhdcaulj',
            title='vwzbjyrgsywuuhuhdzow'
        )
        return instance

    
    def test_rel_property(self):
        """
        Test rel property
        """
        test_value = 'etsudihnlueoyrysabbq'
        self.instance.rel = test_value
        self.assertEqual(self.instance.rel, test_value)
    
    def test_href_property(self):
        """
        Test href property
        """
        test_value = 'vzlnblswiixzrpmkbxte'
        self.instance.href = test_value
        self.assertEqual(self.instance.href, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'fxcsjfozrfjxwhdcaulj'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'vwzbjyrgsywuuhuhdzow'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Link.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Link.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

