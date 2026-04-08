"""
Test case for Component
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from luchtmeetnet_nl_producer_data.nl.rivm.luchtmeetnet.components.component import Component


class Test_Component(unittest.TestCase):
    """
    Test case for Component
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Component.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Component for testing
        """
        instance = Component(
            formula='pkxclbyxzchpqoadheiw',
            name_nl='tlujxuzktnhdotabkdun',
            name_en='nuatwbmbtxwtujrycuml'
        )
        return instance

    
    def test_formula_property(self):
        """
        Test formula property
        """
        test_value = 'pkxclbyxzchpqoadheiw'
        self.instance.formula = test_value
        self.assertEqual(self.instance.formula, test_value)
    
    def test_name_nl_property(self):
        """
        Test name_nl property
        """
        test_value = 'tlujxuzktnhdotabkdun'
        self.instance.name_nl = test_value
        self.assertEqual(self.instance.name_nl, test_value)
    
    def test_name_en_property(self):
        """
        Test name_en property
        """
        test_value = 'nuatwbmbtxwtujrycuml'
        self.instance.name_en = test_value
        self.assertEqual(self.instance.name_en, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Component.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
