"""
Test case for Salinity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.salinity import Salinity


class Test_Salinity(unittest.TestCase):
    """
    Test case for Salinity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Salinity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Salinity for testing
        """
        instance = Salinity(
            site_no='ckmaearozgjzubzdahro',
            datetime='xmsvtzdgryhtxouxkums',
            value=float(11.57365868082534),
            exception='jqwbmcjohzvbjlewnjti',
            qualifiers=['muitwkwyyrvmtmeyoyyl', 'xtjlzkhnxllzcorclfyk', 'yxbtmszshprldxnnystm'],
            parameter_cd='orpkovavqkictfyqmdnv',
            timeseries_cd='nxjzljzrpxhnxbwnofgy'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'ckmaearozgjzubzdahro'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'xmsvtzdgryhtxouxkums'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(11.57365868082534)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'jqwbmcjohzvbjlewnjti'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['muitwkwyyrvmtmeyoyyl', 'xtjlzkhnxllzcorclfyk', 'yxbtmszshprldxnnystm']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'orpkovavqkictfyqmdnv'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'nxjzljzrpxhnxbwnofgy'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Salinity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Salinity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

