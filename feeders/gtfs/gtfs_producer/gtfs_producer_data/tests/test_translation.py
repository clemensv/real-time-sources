"""
Test case for Translation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedrealtime.alert.translatedstring_types.translation import Translation


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
            text='gkfbxiuxzukddidwksgi',
            language='bugjzufzedfrdbiruuso'
        )
        return instance

    
    def test_text_property(self):
        """
        Test text property
        """
        test_value = 'gkfbxiuxzukddidwksgi'
        self.instance.text = test_value
        self.assertEqual(self.instance.text, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'bugjzufzedfrdbiruuso'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Translation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Translation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

