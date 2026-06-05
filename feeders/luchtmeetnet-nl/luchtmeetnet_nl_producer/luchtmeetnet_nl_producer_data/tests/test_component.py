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
            formula='cvcnclmfhweontgrgtfs',
            name_nl='xiwldbqiicfogihqzhhk',
            name_en='rfbczclhwtcaqksixtnc'
        )
        return instance

    
    def test_formula_property(self):
        """
        Test formula property
        """
        test_value = 'cvcnclmfhweontgrgtfs'
        self.instance.formula = test_value
        self.assertEqual(self.instance.formula, test_value)
    
    def test_name_nl_property(self):
        """
        Test name_nl property
        """
        test_value = 'xiwldbqiicfogihqzhhk'
        self.instance.name_nl = test_value
        self.assertEqual(self.instance.name_nl, test_value)
    
    def test_name_en_property(self):
        """
        Test name_en property
        """
        test_value = 'rfbczclhwtcaqksixtnc'
        self.instance.name_en = test_value
        self.assertEqual(self.instance.name_en, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Component.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Component.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

