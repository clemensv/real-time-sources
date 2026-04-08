"""
Test case for XrayFlare
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.microsoft.opendata.us.noaa.swpc.xrayflare import XrayFlare


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
            time_tag='uozhsgjbxuvgwmyaadvf',
            begin_time='mvapjbfuohduxxlgqbte',
            begin_class='fyhgprtlnfliqghizrvk',
            max_time='qcviuplhqgvignovoqzr',
            max_class='debiulzzxaqyfiruhakv',
            max_xrlong=float(32.27149491441889),
            max_ratio=float(71.46179227770128),
            max_ratio_time='ozgqkmcxcfhpslmjxjen',
            current_int_xrlong=float(78.10829746691746),
            end_time='bdvexjjrezlohudevjrd',
            end_class='xkqzjstsatbffshtljbf',
            satellite=int(56)
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'uozhsgjbxuvgwmyaadvf'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_begin_time_property(self):
        """
        Test begin_time property
        """
        test_value = 'mvapjbfuohduxxlgqbte'
        self.instance.begin_time = test_value
        self.assertEqual(self.instance.begin_time, test_value)
    
    def test_begin_class_property(self):
        """
        Test begin_class property
        """
        test_value = 'fyhgprtlnfliqghizrvk'
        self.instance.begin_class = test_value
        self.assertEqual(self.instance.begin_class, test_value)
    
    def test_max_time_property(self):
        """
        Test max_time property
        """
        test_value = 'qcviuplhqgvignovoqzr'
        self.instance.max_time = test_value
        self.assertEqual(self.instance.max_time, test_value)
    
    def test_max_class_property(self):
        """
        Test max_class property
        """
        test_value = 'debiulzzxaqyfiruhakv'
        self.instance.max_class = test_value
        self.assertEqual(self.instance.max_class, test_value)
    
    def test_max_xrlong_property(self):
        """
        Test max_xrlong property
        """
        test_value = float(32.27149491441889)
        self.instance.max_xrlong = test_value
        self.assertEqual(self.instance.max_xrlong, test_value)
    
    def test_max_ratio_property(self):
        """
        Test max_ratio property
        """
        test_value = float(71.46179227770128)
        self.instance.max_ratio = test_value
        self.assertEqual(self.instance.max_ratio, test_value)
    
    def test_max_ratio_time_property(self):
        """
        Test max_ratio_time property
        """
        test_value = 'ozgqkmcxcfhpslmjxjen'
        self.instance.max_ratio_time = test_value
        self.assertEqual(self.instance.max_ratio_time, test_value)
    
    def test_current_int_xrlong_property(self):
        """
        Test current_int_xrlong property
        """
        test_value = float(78.10829746691746)
        self.instance.current_int_xrlong = test_value
        self.assertEqual(self.instance.current_int_xrlong, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'bdvexjjrezlohudevjrd'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_end_class_property(self):
        """
        Test end_class property
        """
        test_value = 'xkqzjstsatbffshtljbf'
        self.instance.end_class = test_value
        self.assertEqual(self.instance.end_class, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(56)
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = XrayFlare.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
