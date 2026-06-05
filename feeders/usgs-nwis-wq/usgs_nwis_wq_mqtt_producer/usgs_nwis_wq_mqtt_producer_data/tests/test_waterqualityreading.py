"""
Test case for WaterQualityReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_nwis_wq_mqtt_producer_data.waterqualityreading import WaterQualityReading


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
            site_number='ndgcgvusagkuzfsdxoxj',
            site_name='agfhmkbbmteummlykqok',
            parameter_code='buckhpioiiuptokykwrh',
            parameter_name='vhqpeknepvcqvvhemzgl',
            value=float(52.90191563310566),
            unit='qgkguxpdsibanfdgsgor',
            qualifier='agtomwhtegmunoljiuyp',
            date_time='yzlqsrzlmmthieucysig',
            state='vhpljyjgvmshnbmlpuha'
        )
        return instance

    
    def test_site_number_property(self):
        """
        Test site_number property
        """
        test_value = 'ndgcgvusagkuzfsdxoxj'
        self.instance.site_number = test_value
        self.assertEqual(self.instance.site_number, test_value)
    
    def test_site_name_property(self):
        """
        Test site_name property
        """
        test_value = 'agfhmkbbmteummlykqok'
        self.instance.site_name = test_value
        self.assertEqual(self.instance.site_name, test_value)
    
    def test_parameter_code_property(self):
        """
        Test parameter_code property
        """
        test_value = 'buckhpioiiuptokykwrh'
        self.instance.parameter_code = test_value
        self.assertEqual(self.instance.parameter_code, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'vhqpeknepvcqvvhemzgl'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(52.90191563310566)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'qgkguxpdsibanfdgsgor'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_qualifier_property(self):
        """
        Test qualifier property
        """
        test_value = 'agtomwhtegmunoljiuyp'
        self.instance.qualifier = test_value
        self.assertEqual(self.instance.qualifier, test_value)
    
    def test_date_time_property(self):
        """
        Test date_time property
        """
        test_value = 'yzlqsrzlmmthieucysig'
        self.instance.date_time = test_value
        self.assertEqual(self.instance.date_time, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'vhpljyjgvmshnbmlpuha'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterQualityReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterQualityReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

