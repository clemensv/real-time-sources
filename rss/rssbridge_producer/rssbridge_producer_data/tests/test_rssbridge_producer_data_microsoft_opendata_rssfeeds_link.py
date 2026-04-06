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
            rel='ycnmlkewsfekaheapdjc',
            href='zxagivudwvwbuauetkbc',
            type='dzzmpatueqdxyhrzztiv',
            title='icstxnssszkbadeaumea'
        )
        return instance

    
    def test_rel_property(self):
        """
        Test rel property
        """
        test_value = 'ycnmlkewsfekaheapdjc'
        self.instance.rel = test_value
        self.assertEqual(self.instance.rel, test_value)
    
    def test_href_property(self):
        """
        Test href property
        """
        test_value = 'zxagivudwvwbuauetkbc'
        self.instance.href = test_value
        self.assertEqual(self.instance.href, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'dzzmpatueqdxyhrzztiv'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'icstxnssszkbadeaumea'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Link.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
