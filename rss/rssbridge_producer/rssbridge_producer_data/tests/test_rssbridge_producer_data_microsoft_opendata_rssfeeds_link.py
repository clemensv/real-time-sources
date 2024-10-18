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
            rel='eptwlrtpvquksfjssguc',
            href='zftfcdttnkjertksrhiy',
            type='bkslvlzosiunacszjcdu',
            title='zaslhewnevivipuwsqyc'
        )
        return instance

    
    def test_rel_property(self):
        """
        Test rel property
        """
        test_value = 'eptwlrtpvquksfjssguc'
        self.instance.rel = test_value
        self.assertEqual(self.instance.rel, test_value)
    
    def test_href_property(self):
        """
        Test href property
        """
        test_value = 'zftfcdttnkjertksrhiy'
        self.instance.href = test_value
        self.assertEqual(self.instance.href, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'bkslvlzosiunacszjcdu'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'zaslhewnevivipuwsqyc'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
