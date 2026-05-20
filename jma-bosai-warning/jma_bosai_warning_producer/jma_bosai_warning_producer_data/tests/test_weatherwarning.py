"""
Test case for WeatherWarning
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.weatherwarning import WeatherWarning
from jma_bosai_warning_producer_data.warningitem import WarningItem


class Test_WeatherWarning(unittest.TestCase):
    """
    Test case for WeatherWarning
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherWarning.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherWarning for testing
        """
        instance = WeatherWarning(
            office_code='nvwxpzwbyrxcjfxkvkgo',
            area_code='uxqiyexcyccvtzubfbvq',
            area_name='dinelvxqucpnzhucgiok',
            report_datetime='pubpllflrybuwdtxtsvs',
            report_datetime_local='fszpsafomucciscxbxxr',
            headline_text='udnziwhrwkqsyohkjufx',
            warnings=[None, None, None, None, None],
            time_defines=['vsbnloqzrpwicmbveygd', 'hcewqmqyinnridkfjnlb', 'jxblojkgzxdsuxijrgtn', 'bnsmwojcxiybldwkfzzo']
        )
        return instance

    
    def test_office_code_property(self):
        """
        Test office_code property
        """
        test_value = 'nvwxpzwbyrxcjfxkvkgo'
        self.instance.office_code = test_value
        self.assertEqual(self.instance.office_code, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'uxqiyexcyccvtzubfbvq'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_area_name_property(self):
        """
        Test area_name property
        """
        test_value = 'dinelvxqucpnzhucgiok'
        self.instance.area_name = test_value
        self.assertEqual(self.instance.area_name, test_value)
    
    def test_report_datetime_property(self):
        """
        Test report_datetime property
        """
        test_value = 'pubpllflrybuwdtxtsvs'
        self.instance.report_datetime = test_value
        self.assertEqual(self.instance.report_datetime, test_value)
    
    def test_report_datetime_local_property(self):
        """
        Test report_datetime_local property
        """
        test_value = 'fszpsafomucciscxbxxr'
        self.instance.report_datetime_local = test_value
        self.assertEqual(self.instance.report_datetime_local, test_value)
    
    def test_headline_text_property(self):
        """
        Test headline_text property
        """
        test_value = 'udnziwhrwkqsyohkjufx'
        self.instance.headline_text = test_value
        self.assertEqual(self.instance.headline_text, test_value)
    
    def test_warnings_property(self):
        """
        Test warnings property
        """
        test_value = [None, None, None, None, None]
        self.instance.warnings = test_value
        self.assertEqual(self.instance.warnings, test_value)
    
    def test_time_defines_property(self):
        """
        Test time_defines property
        """
        test_value = ['vsbnloqzrpwicmbveygd', 'hcewqmqyinnridkfjnlb', 'jxblojkgzxdsuxijrgtn', 'bnsmwojcxiybldwkfzzo']
        self.instance.time_defines = test_value
        self.assertEqual(self.instance.time_defines, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherWarning.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherWarning.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

