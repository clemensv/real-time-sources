"""
Test case for Translation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.alert.translatedstring_types.translation import Translation

class Test_Translation(unittest.TestCase):
    """
    Test case for Translation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Translation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Translation for testing
        """
        instance = Translation(
            text='qhdobstwihqogztqnlvc',
            language='fuwzcmfmekcbztadpebp'
        )
        return instance

    
    def test_text_property(self):
        """
        Test text property
        """
        test_value = 'qhdobstwihqogztqnlvc'
        self.instance.text = test_value
        self.assertEqual(self.instance.text, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'fuwzcmfmekcbztadpebp'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
