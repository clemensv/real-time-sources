"""
Test case for WaterVelocity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.watervelocity import WaterVelocity


class Test_WaterVelocity(unittest.TestCase):
    """
    Test case for WaterVelocity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterVelocity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterVelocity for testing
        """
        instance = WaterVelocity(
            site_no='nnlumgwlvonrzgjfinsf',
            datetime='symcawrbelktznxbegfw',
            value=float(32.34627288896975),
            exception='pqkhmjibhejgxvncxsfu',
            qualifiers=['mikaqjtiyqfzxsctxbhw', 'urtiyahmhkgzvktoidhx'],
            parameter_cd='qdhngddksktzezbqtlxm',
            timeseries_cd='pedzwkgdkopdodedyeqm'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'nnlumgwlvonrzgjfinsf'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'symcawrbelktznxbegfw'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(32.34627288896975)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'pqkhmjibhejgxvncxsfu'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['mikaqjtiyqfzxsctxbhw', 'urtiyahmhkgzvktoidhx']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'qdhngddksktzezbqtlxm'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'pedzwkgdkopdodedyeqm'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
