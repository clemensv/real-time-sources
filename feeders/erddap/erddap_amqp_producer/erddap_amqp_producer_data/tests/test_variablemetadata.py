"""
Test case for VariableMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from erddap_amqp_producer_data.variablemetadata import VariableMetadata


class Test_VariableMetadata(unittest.TestCase):
    """
    Test case for VariableMetadata
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VariableMetadata.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VariableMetadata for testing
        """
        instance = VariableMetadata(
            name='fnagghucyadbdxwhyuqd',
            data_type='ybowpqsbymqnonyompeg',
            unit='yfbkuczmzalcrkhaygdf',
            long_name='ruvcruvoyrugiwuzlqoa',
            standard_name='toqivntzrttumzejsrnf',
            ioos_category='zphcyzrvigkdhwmcqgxg',
            cf_role='abzfbomtktuojbyadgbv'
        )
        return instance

    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'fnagghucyadbdxwhyuqd'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_data_type_property(self):
        """
        Test data_type property
        """
        test_value = 'ybowpqsbymqnonyompeg'
        self.instance.data_type = test_value
        self.assertEqual(self.instance.data_type, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'yfbkuczmzalcrkhaygdf'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_long_name_property(self):
        """
        Test long_name property
        """
        test_value = 'ruvcruvoyrugiwuzlqoa'
        self.instance.long_name = test_value
        self.assertEqual(self.instance.long_name, test_value)
    
    def test_standard_name_property(self):
        """
        Test standard_name property
        """
        test_value = 'toqivntzrttumzejsrnf'
        self.instance.standard_name = test_value
        self.assertEqual(self.instance.standard_name, test_value)
    
    def test_ioos_category_property(self):
        """
        Test ioos_category property
        """
        test_value = 'zphcyzrvigkdhwmcqgxg'
        self.instance.ioos_category = test_value
        self.assertEqual(self.instance.ioos_category, test_value)
    
    def test_cf_role_property(self):
        """
        Test cf_role property
        """
        test_value = 'abzfbomtktuojbyadgbv'
        self.instance.cf_role = test_value
        self.assertEqual(self.instance.cf_role, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VariableMetadata.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VariableMetadata.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

