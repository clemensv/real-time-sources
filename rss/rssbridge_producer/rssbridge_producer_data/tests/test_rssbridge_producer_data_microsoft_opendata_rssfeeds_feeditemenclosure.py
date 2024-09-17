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
            href='kwebonxarzmyngxniwza',
            length=int(59),
            type='dwolpsdjgbxzdbunkype'
        )
        return instance

    
    def test_href_property(self):
        """
        Test href property
        """
        test_value = 'kwebonxarzmyngxniwza'
        self.instance.href = test_value
        self.assertEqual(self.instance.href, test_value)
    
    def test_length_property(self):
        """
        Test length property
        """
        test_value = int(59)
        self.instance.length = test_value
        self.assertEqual(self.instance.length, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'dwolpsdjgbxzdbunkype'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
