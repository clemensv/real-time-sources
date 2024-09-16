"""
Test case for FeedItemContent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemcontent import FeedItemContent

class Test_FeedItemContent(unittest.TestCase):
    """
    Test case for FeedItemContent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItemContent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItemContent for testing
        """
        instance = FeedItemContent(
            value='vwpqtbfesuldeianondj',
            type='umrijkptlzojwhbaoncu',
            language='ulngcyqapuvknbsredbu',
            base='qxprfgvubtyhbevrrhac'
        )
        return instance

    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = 'vwpqtbfesuldeianondj'
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'umrijkptlzojwhbaoncu'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'ulngcyqapuvknbsredbu'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_base_property(self):
        """
        Test base property
        """
        test_value = 'qxprfgvubtyhbevrrhac'
        self.instance.base = test_value
        self.assertEqual(self.instance.base, test_value)
    
