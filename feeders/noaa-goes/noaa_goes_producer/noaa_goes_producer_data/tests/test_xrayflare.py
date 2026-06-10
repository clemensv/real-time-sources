"""
Test case for XrayFlare
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.xrayflare import XrayFlare


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
            time_tag='elpqmnwtldlfsdjfaejt',
            begin_time='zsbombrlubgcqixsynlq',
            begin_class='ccdqiflxusyysetpbsfy',
            max_time='rwexvaqhelcbjrvfduzt',
            max_class='ytqinpxfdnuhgupuzqid',
            max_xrlong=float(68.08799709246767),
            max_ratio=float(73.88468782843684),
            max_ratio_time='hsoorpvoifolefoedizk',
            current_int_xrlong=float(66.28620321989831),
            end_time='mauihktnkdggqplugaor',
            end_class='xydvmtnxmeqcsuzqrsmt',
            satellite=int(95)
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'elpqmnwtldlfsdjfaejt'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_begin_time_property(self):
        """
        Test begin_time property
        """
        test_value = 'zsbombrlubgcqixsynlq'
        self.instance.begin_time = test_value
        self.assertEqual(self.instance.begin_time, test_value)
    
    def test_begin_class_property(self):
        """
        Test begin_class property
        """
        test_value = 'ccdqiflxusyysetpbsfy'
        self.instance.begin_class = test_value
        self.assertEqual(self.instance.begin_class, test_value)
    
    def test_max_time_property(self):
        """
        Test max_time property
        """
        test_value = 'rwexvaqhelcbjrvfduzt'
        self.instance.max_time = test_value
        self.assertEqual(self.instance.max_time, test_value)
    
    def test_max_class_property(self):
        """
        Test max_class property
        """
        test_value = 'ytqinpxfdnuhgupuzqid'
        self.instance.max_class = test_value
        self.assertEqual(self.instance.max_class, test_value)
    
    def test_max_xrlong_property(self):
        """
        Test max_xrlong property
        """
        test_value = float(68.08799709246767)
        self.instance.max_xrlong = test_value
        self.assertEqual(self.instance.max_xrlong, test_value)
    
    def test_max_ratio_property(self):
        """
        Test max_ratio property
        """
        test_value = float(73.88468782843684)
        self.instance.max_ratio = test_value
        self.assertEqual(self.instance.max_ratio, test_value)
    
    def test_max_ratio_time_property(self):
        """
        Test max_ratio_time property
        """
        test_value = 'hsoorpvoifolefoedizk'
        self.instance.max_ratio_time = test_value
        self.assertEqual(self.instance.max_ratio_time, test_value)
    
    def test_current_int_xrlong_property(self):
        """
        Test current_int_xrlong property
        """
        test_value = float(66.28620321989831)
        self.instance.current_int_xrlong = test_value
        self.assertEqual(self.instance.current_int_xrlong, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'mauihktnkdggqplugaor'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_end_class_property(self):
        """
        Test end_class property
        """
        test_value = 'xydvmtnxmeqcsuzqrsmt'
        self.instance.end_class = test_value
        self.assertEqual(self.instance.end_class, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(95)
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

