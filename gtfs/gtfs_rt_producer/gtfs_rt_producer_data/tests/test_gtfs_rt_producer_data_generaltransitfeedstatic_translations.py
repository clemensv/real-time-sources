"""
Test case for Translations
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.translations import Translations

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
            tableName='tmwesyajazetqiisqxrh',
            fieldName='sfzzxwikdvmtbctpcuab',
            language='gkkpwtczsraauqhbegbo',
            translation='zlxwlyrsbmmzewusjabs'
        )
        return instance

    
    def test_tableName_property(self):
        """
        Test tableName property
        """
        test_value = 'tmwesyajazetqiisqxrh'
        self.instance.tableName = test_value
        self.assertEqual(self.instance.tableName, test_value)
    
    def test_fieldName_property(self):
        """
        Test fieldName property
        """
        test_value = 'sfzzxwikdvmtbctpcuab'
        self.instance.fieldName = test_value
        self.assertEqual(self.instance.fieldName, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'gkkpwtczsraauqhbegbo'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_translation_property(self):
        """
        Test translation property
        """
        test_value = 'zlxwlyrsbmmzewusjabs'
        self.instance.translation = test_value
        self.assertEqual(self.instance.translation, test_value)
    
