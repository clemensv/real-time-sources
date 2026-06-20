"""
Test case for MeasurementValue
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from erddap_producer_data.measurementvalue import MeasurementValue


class Test_MeasurementValue(unittest.TestCase):
    """
    Test case for MeasurementValue
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MeasurementValue.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MeasurementValue for testing
        """
        instance = MeasurementValue(
            variable_name='gmvpfcnossodeyyioxbd',
            value_double=float(9.059129668980892),
            value_string='cbhhxelckcpxlplmbfhg',
            unit='bhrjmaglodmvpiwiyjdw',
            long_name='btemuvoexccimeiudppd',
            standard_name='gvjrjkzyuxpalfyhzufh',
            ioos_category='qtyiottmphhdddletqru',
            quality_flag='jbayvexrtgjhudunsftb'
        )
        return instance

    
    def test_variable_name_property(self):
        """
        Test variable_name property
        """
        test_value = 'gmvpfcnossodeyyioxbd'
        self.instance.variable_name = test_value
        self.assertEqual(self.instance.variable_name, test_value)
    
    def test_value_double_property(self):
        """
        Test value_double property
        """
        test_value = float(9.059129668980892)
        self.instance.value_double = test_value
        self.assertEqual(self.instance.value_double, test_value)
    
    def test_value_string_property(self):
        """
        Test value_string property
        """
        test_value = 'cbhhxelckcpxlplmbfhg'
        self.instance.value_string = test_value
        self.assertEqual(self.instance.value_string, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'bhrjmaglodmvpiwiyjdw'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_long_name_property(self):
        """
        Test long_name property
        """
        test_value = 'btemuvoexccimeiudppd'
        self.instance.long_name = test_value
        self.assertEqual(self.instance.long_name, test_value)
    
    def test_standard_name_property(self):
        """
        Test standard_name property
        """
        test_value = 'gvjrjkzyuxpalfyhzufh'
        self.instance.standard_name = test_value
        self.assertEqual(self.instance.standard_name, test_value)
    
    def test_ioos_category_property(self):
        """
        Test ioos_category property
        """
        test_value = 'qtyiottmphhdddletqru'
        self.instance.ioos_category = test_value
        self.assertEqual(self.instance.ioos_category, test_value)
    
    def test_quality_flag_property(self):
        """
        Test quality_flag property
        """
        test_value = 'jbayvexrtgjhudunsftb'
        self.instance.quality_flag = test_value
        self.assertEqual(self.instance.quality_flag, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MeasurementValue.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MeasurementValue.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

