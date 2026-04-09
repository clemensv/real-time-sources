"""
Test case for WaterQualityReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_nwis_wq_producer_data.usgs_nwis_wq_producer_data.waterqualityreading import WaterQualityReading


class Test_WaterQualityReading(unittest.TestCase):
    """
    Test case for WaterQualityReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterQualityReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterQualityReading for testing
        """
        instance = WaterQualityReading(
            site_number='txxwaxagefohvekptdxp',
            site_name='afcixkatcrgerbovxelh',
            parameter_code='qmdanawaudreuopdthlw',
            parameter_name='rlyjbyjfvcnsapelyxvy',
            value=float(42.09335089418504),
            unit='nnhlxzpuemxmimaubpwn',
            qualifier='vdbmhgrpqqhzzfeszbsx',
            date_time='auixutlzqrlkmrchvsxt'
        )
        return instance

    
    def test_site_number_property(self):
        """
        Test site_number property
        """
        test_value = 'txxwaxagefohvekptdxp'
        self.instance.site_number = test_value
        self.assertEqual(self.instance.site_number, test_value)
    
    def test_site_name_property(self):
        """
        Test site_name property
        """
        test_value = 'afcixkatcrgerbovxelh'
        self.instance.site_name = test_value
        self.assertEqual(self.instance.site_name, test_value)
    
    def test_parameter_code_property(self):
        """
        Test parameter_code property
        """
        test_value = 'qmdanawaudreuopdthlw'
        self.instance.parameter_code = test_value
        self.assertEqual(self.instance.parameter_code, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'rlyjbyjfvcnsapelyxvy'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(42.09335089418504)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'nnhlxzpuemxmimaubpwn'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_qualifier_property(self):
        """
        Test qualifier property
        """
        test_value = 'vdbmhgrpqqhzzfeszbsx'
        self.instance.qualifier = test_value
        self.assertEqual(self.instance.qualifier, test_value)
    
    def test_date_time_property(self):
        """
        Test date_time property
        """
        test_value = 'auixutlzqrlkmrchvsxt'
        self.instance.date_time = test_value
        self.assertEqual(self.instance.date_time, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterQualityReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
