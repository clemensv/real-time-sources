"""
Test case for XrayFlare
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_mqtt_producer_data.xrayflare import XrayFlare


class Test_XrayFlare(unittest.TestCase):
    """
    Test case for XrayFlare
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_XrayFlare.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of XrayFlare for testing
        """
        instance = XrayFlare(
            time_tag='qcqpdlrnviqhuxdmfgwd',
            begin_time='ylbsraghknbfkdviwcim',
            begin_class='mkibutuolspilyfatidd',
            max_time='ichktqwzfbxnfmxljlrq',
            max_class='ayomqxbpsxepuqwhxgwb',
            max_xrlong=float(6.523190857649697),
            max_ratio=float(61.458495543671766),
            max_ratio_time='kqizasfyjjorfqjmrmud',
            current_int_xrlong=float(58.76978185819826),
            end_time='jezvhifpjvxirqvatbio',
            end_class='mesvisuciraqhwjnsmwi',
            satellite=int(96)
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'qcqpdlrnviqhuxdmfgwd'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_begin_time_property(self):
        """
        Test begin_time property
        """
        test_value = 'ylbsraghknbfkdviwcim'
        self.instance.begin_time = test_value
        self.assertEqual(self.instance.begin_time, test_value)
    
    def test_begin_class_property(self):
        """
        Test begin_class property
        """
        test_value = 'mkibutuolspilyfatidd'
        self.instance.begin_class = test_value
        self.assertEqual(self.instance.begin_class, test_value)
    
    def test_max_time_property(self):
        """
        Test max_time property
        """
        test_value = 'ichktqwzfbxnfmxljlrq'
        self.instance.max_time = test_value
        self.assertEqual(self.instance.max_time, test_value)
    
    def test_max_class_property(self):
        """
        Test max_class property
        """
        test_value = 'ayomqxbpsxepuqwhxgwb'
        self.instance.max_class = test_value
        self.assertEqual(self.instance.max_class, test_value)
    
    def test_max_xrlong_property(self):
        """
        Test max_xrlong property
        """
        test_value = float(6.523190857649697)
        self.instance.max_xrlong = test_value
        self.assertEqual(self.instance.max_xrlong, test_value)
    
    def test_max_ratio_property(self):
        """
        Test max_ratio property
        """
        test_value = float(61.458495543671766)
        self.instance.max_ratio = test_value
        self.assertEqual(self.instance.max_ratio, test_value)
    
    def test_max_ratio_time_property(self):
        """
        Test max_ratio_time property
        """
        test_value = 'kqizasfyjjorfqjmrmud'
        self.instance.max_ratio_time = test_value
        self.assertEqual(self.instance.max_ratio_time, test_value)
    
    def test_current_int_xrlong_property(self):
        """
        Test current_int_xrlong property
        """
        test_value = float(58.76978185819826)
        self.instance.current_int_xrlong = test_value
        self.assertEqual(self.instance.current_int_xrlong, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'jezvhifpjvxirqvatbio'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_end_class_property(self):
        """
        Test end_class property
        """
        test_value = 'mesvisuciraqhwjnsmwi'
        self.instance.end_class = test_value
        self.assertEqual(self.instance.end_class, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(96)
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = XrayFlare.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = XrayFlare.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

