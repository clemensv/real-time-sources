"""
Test case for TranslatedString
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedrealtime.alert.translatedstring import TranslatedString
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.alert.translatedstring_types.translation import Translation


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
            translation=[None, None, None]
        )
        return instance

    
    def test_translation_property(self):
        """
        Test translation property
        """
        test_value = [None, None, None]
        self.instance.translation = test_value
        self.assertEqual(self.instance.translation, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TranslatedString.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TranslatedString.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

