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
            time_tag='yiijrdenvczxypkcdqth',
            begin_time='xekoojioorhvfsqdokgk',
            begin_class='tojgsjcycckhybhdsjgz',
            max_time='gejnxfvpkbwheypfflcd',
            max_class='rmndbyklgfnbopcxtnka',
            max_xrlong=float(29.983259408219),
            max_ratio=float(29.884006787119766),
            max_ratio_time='eouevtthftkpgpwobxee',
            current_int_xrlong=float(67.57544121730777),
            end_time='jnkdiwjzfdznwzptqnpq',
            end_class='towbuvuzzcnqxptbqsrs',
            satellite=int(97)
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'yiijrdenvczxypkcdqth'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_begin_time_property(self):
        """
        Test begin_time property
        """
        test_value = 'xekoojioorhvfsqdokgk'
        self.instance.begin_time = test_value
        self.assertEqual(self.instance.begin_time, test_value)
    
    def test_begin_class_property(self):
        """
        Test begin_class property
        """
        test_value = 'tojgsjcycckhybhdsjgz'
        self.instance.begin_class = test_value
        self.assertEqual(self.instance.begin_class, test_value)
    
    def test_max_time_property(self):
        """
        Test max_time property
        """
        test_value = 'gejnxfvpkbwheypfflcd'
        self.instance.max_time = test_value
        self.assertEqual(self.instance.max_time, test_value)
    
    def test_max_class_property(self):
        """
        Test max_class property
        """
        test_value = 'rmndbyklgfnbopcxtnka'
        self.instance.max_class = test_value
        self.assertEqual(self.instance.max_class, test_value)
    
    def test_max_xrlong_property(self):
        """
        Test max_xrlong property
        """
        test_value = float(29.983259408219)
        self.instance.max_xrlong = test_value
        self.assertEqual(self.instance.max_xrlong, test_value)
    
    def test_max_ratio_property(self):
        """
        Test max_ratio property
        """
        test_value = float(29.884006787119766)
        self.instance.max_ratio = test_value
        self.assertEqual(self.instance.max_ratio, test_value)
    
    def test_max_ratio_time_property(self):
        """
        Test max_ratio_time property
        """
        test_value = 'eouevtthftkpgpwobxee'
        self.instance.max_ratio_time = test_value
        self.assertEqual(self.instance.max_ratio_time, test_value)
    
    def test_current_int_xrlong_property(self):
        """
        Test current_int_xrlong property
        """
        test_value = float(67.57544121730777)
        self.instance.current_int_xrlong = test_value
        self.assertEqual(self.instance.current_int_xrlong, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'jnkdiwjzfdznwzptqnpq'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_end_class_property(self):
        """
        Test end_class property
        """
        test_value = 'towbuvuzzcnqxptbqsrs'
        self.instance.end_class = test_value
        self.assertEqual(self.instance.end_class, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(97)
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

