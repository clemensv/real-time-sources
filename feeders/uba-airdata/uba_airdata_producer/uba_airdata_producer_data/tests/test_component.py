"""
Test case for Component
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uba_airdata_producer_data.de.uba.airdata.components.component import Component


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
            component_id=int(16),
            component_code='rdrlowsrxzzyujszkhol',
            symbol='chpizdsarlgudvxmvnan',
            unit='xjuxrfkecrgarfecamds',
            name='vwxcwcgdizcnhzibtcvr'
        )
        return instance

    
    def test_component_id_property(self):
        """
        Test component_id property
        """
        test_value = int(16)
        self.instance.component_id = test_value
        self.assertEqual(self.instance.component_id, test_value)
    
    def test_component_code_property(self):
        """
        Test component_code property
        """
        test_value = 'rdrlowsrxzzyujszkhol'
        self.instance.component_code = test_value
        self.assertEqual(self.instance.component_code, test_value)
    
    def test_symbol_property(self):
        """
        Test symbol property
        """
        test_value = 'chpizdsarlgudvxmvnan'
        self.instance.symbol = test_value
        self.assertEqual(self.instance.symbol, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'xjuxrfkecrgarfecamds'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'vwxcwcgdizcnhzibtcvr'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
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

