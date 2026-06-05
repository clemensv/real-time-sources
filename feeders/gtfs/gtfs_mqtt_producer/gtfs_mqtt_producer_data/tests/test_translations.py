"""
Test case for Translations
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.translations import Translations


class Test_Translations(unittest.TestCase):
    """
    Test case for Translations
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Translations.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Translations for testing
        """
        instance = Translations(
            tableName='raktshevtysmotdgugsc',
            fieldName='zgwcocijkpiekxxftzzc',
            language='xshurngaqthjxjfylrkd',
            translation='prkunohrbsckbzmhtjcy'
        )
        return instance

    
    def test_tableName_property(self):
        """
        Test tableName property
        """
        test_value = 'raktshevtysmotdgugsc'
        self.instance.tableName = test_value
        self.assertEqual(self.instance.tableName, test_value)
    
    def test_fieldName_property(self):
        """
        Test fieldName property
        """
        test_value = 'zgwcocijkpiekxxftzzc'
        self.instance.fieldName = test_value
        self.assertEqual(self.instance.fieldName, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'xshurngaqthjxjfylrkd'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_translation_property(self):
        """
        Test translation property
        """
        test_value = 'prkunohrbsckbzmhtjcy'
        self.instance.translation = test_value
        self.assertEqual(self.instance.translation, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Translations.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Translations.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

