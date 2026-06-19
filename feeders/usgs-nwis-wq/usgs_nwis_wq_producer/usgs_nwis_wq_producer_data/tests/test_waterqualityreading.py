"""
Test case for WaterQualityReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_nwis_wq_producer_data.waterqualityreading import WaterQualityReading


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
            site_number='kzyijfsgmvsoakjkeiad',
            site_name='qpzobnewhrjsxwwcyslk',
            parameter_code='lirvyzdakinzhyfgsfra',
            parameter_name='guulhqxbdysktbkqlihs',
            value=float(6.289565346954218),
            unit='toqekbuxhrlnbjmtydpo',
            qualifier='buwevxtzzyvkpdjezcyp',
            date_time='pelilfgkdbjhjjnfdryd',
            state='cebhvkxofugwzajjgisx'
        )
        return instance

    
    def test_site_number_property(self):
        """
        Test site_number property
        """
        test_value = 'kzyijfsgmvsoakjkeiad'
        self.instance.site_number = test_value
        self.assertEqual(self.instance.site_number, test_value)
    
    def test_site_name_property(self):
        """
        Test site_name property
        """
        test_value = 'qpzobnewhrjsxwwcyslk'
        self.instance.site_name = test_value
        self.assertEqual(self.instance.site_name, test_value)
    
    def test_parameter_code_property(self):
        """
        Test parameter_code property
        """
        test_value = 'lirvyzdakinzhyfgsfra'
        self.instance.parameter_code = test_value
        self.assertEqual(self.instance.parameter_code, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'guulhqxbdysktbkqlihs'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(6.289565346954218)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'toqekbuxhrlnbjmtydpo'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_qualifier_property(self):
        """
        Test qualifier property
        """
        test_value = 'buwevxtzzyvkpdjezcyp'
        self.instance.qualifier = test_value
        self.assertEqual(self.instance.qualifier, test_value)
    
    def test_date_time_property(self):
        """
        Test date_time property
        """
        test_value = 'pelilfgkdbjhjjnfdryd'
        self.instance.date_time = test_value
        self.assertEqual(self.instance.date_time, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'cebhvkxofugwzajjgisx'
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

