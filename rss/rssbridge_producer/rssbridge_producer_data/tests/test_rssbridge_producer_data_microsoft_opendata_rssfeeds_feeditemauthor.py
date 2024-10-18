"""
Test case for FeedItemAuthor
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor


class Test_FeedItemAuthor(unittest.TestCase):
    """
    Test case for FeedItemAuthor
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItemAuthor.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItemAuthor for testing
        """
        instance = FeedItemAuthor(
            name='xhgfzmvjoxoxesrxxrkm',
            href='yajnooxxpbqdxutdcend',
            email='rchfqjhzomymbanuhapl'
        )
        return instance

    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xhgfzmvjoxoxesrxxrkm'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_href_property(self):
        """
        Test href property
        """
        test_value = 'yajnooxxpbqdxutdcend'
        self.instance.href = test_value
        self.assertEqual(self.instance.href, test_value)
    
    def test_email_property(self):
        """
        Test email property
        """
        test_value = 'rchfqjhzomymbanuhapl'
        self.instance.email = test_value
        self.assertEqual(self.instance.email, test_value)
    
