"""
Test case for FeedItemPublisher
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditempublisher import FeedItemPublisher


class Test_FeedItemPublisher(unittest.TestCase):
    """
    Test case for FeedItemPublisher
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItemPublisher.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItemPublisher for testing
        """
        instance = FeedItemPublisher(
            name='gnrjlaapyiclmexioyjx',
            href='uetjqvwcblypurwseknq',
            email='pvpxbzjxaomigrhayxjh'
        )
        return instance

    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'gnrjlaapyiclmexioyjx'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_href_property(self):
        """
        Test href property
        """
        test_value = 'uetjqvwcblypurwseknq'
        self.instance.href = test_value
        self.assertEqual(self.instance.href, test_value)
    
    def test_email_property(self):
        """
        Test email property
        """
        test_value = 'pvpxbzjxaomigrhayxjh'
        self.instance.email = test_value
        self.assertEqual(self.instance.email, test_value)
    
