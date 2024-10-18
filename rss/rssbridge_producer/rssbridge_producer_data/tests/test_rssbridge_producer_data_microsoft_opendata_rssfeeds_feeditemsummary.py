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
            value='xlsfvydrrcuwwvobxhyn',
            type='ikytqdxddpssxymlrcif',
            language='vsmwwmbkspyeepcbtsus',
            base='hmsysynbumqibugovqji'
        )
        return instance

    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = 'xlsfvydrrcuwwvobxhyn'
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'ikytqdxddpssxymlrcif'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'vsmwwmbkspyeepcbtsus'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_base_property(self):
        """
        Test base property
        """
        test_value = 'hmsysynbumqibugovqji'
        self.instance.base = test_value
        self.assertEqual(self.instance.base, test_value)
    
