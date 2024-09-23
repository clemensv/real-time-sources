"""
Test case for PH
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.ph import PH


class Test_PH(unittest.TestCase):
    """
    Test case for PH
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PH.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PH for testing
        """
        instance = PH(
            site_no='vvnxvrwucoxqcwdwzzls',
            datetime='tqcebufefnsqsfaidhky',
            value=float(97.94436822937325),
            qualifiers=['xbcnxqhglyxojxdwhpcl', 'liecpkdvgitunfacbjvv', 'gcqcijywrdvhsucneied'],
            parameter_cd='oquasokbneiwriekjjow',
            timeseries_cd='ijohalsbyzqtnqdklezm'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'vvnxvrwucoxqcwdwzzls'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'tqcebufefnsqsfaidhky'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(97.94436822937325)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['xbcnxqhglyxojxdwhpcl', 'liecpkdvgitunfacbjvv', 'gcqcijywrdvhsucneied']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'oquasokbneiwriekjjow'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ijohalsbyzqtnqdklezm'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
