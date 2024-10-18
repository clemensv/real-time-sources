"""
Test case for TranslatedString
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.translatedstring import TranslatedString
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_alert_translatedstring_types_translation import Test_Translation


class Test_TranslatedString(unittest.TestCase):
    """
    Test case for TranslatedString
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TranslatedString.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TranslatedString for testing
        """
        instance = TranslatedString(
            translation=[Test_Translation.create_instance(), Test_Translation.create_instance(), Test_Translation.create_instance(), Test_Translation.create_instance(), Test_Translation.create_instance()]
        )
        return instance

    
    def test_translation_property(self):
        """
        Test translation property
        """
        test_value = [Test_Translation.create_instance(), Test_Translation.create_instance(), Test_Translation.create_instance(), Test_Translation.create_instance(), Test_Translation.create_instance()]
        self.instance.translation = test_value
        self.assertEqual(self.instance.translation, test_value)
    
