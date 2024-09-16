"""
Test case for FeedItemTitle
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle

class Test_FeedItemTitle(unittest.TestCase):
    """
    Test case for FeedItemTitle
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItemTitle.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItemTitle for testing
        """
        instance = FeedItemTitle(
            value='gdhvpcqydnimrwbpznxy',
            type='rwpdbahvrqhhmatxedlu',
            language='yoiyooqwimvwkbuydevs',
            base='hekgdxxrwlsijnhdkrvp'
        )
        return instance

    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = 'gdhvpcqydnimrwbpznxy'
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'rwpdbahvrqhhmatxedlu'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'yoiyooqwimvwkbuydevs'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_base_property(self):
        """
        Test base property
        """
        test_value = 'hekgdxxrwlsijnhdkrvp'
        self.instance.base = test_value
        self.assertEqual(self.instance.base, test_value)
    
