"""
Test case for Turbidity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.turbidity import Turbidity


class Test_Turbidity(unittest.TestCase):
    """
    Test case for Turbidity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Turbidity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Turbidity for testing
        """
        instance = Turbidity(
            site_no='mtanswsdrbyvdqnomukv',
            datetime='wjmhyhyzzbcjaabhahmy',
            value=float(82.71720813915931),
            exception='nifspjhrgulqkzvgjryr',
            qualifiers=['ppgszmbxzgehsughgtdd', 'okzcpcwhyeyrwgcghzeo', 'kllqspsmhzdbpzixqsns'],
            parameter_cd='jbckyrdqelbrhliokpil',
            timeseries_cd='zfannvbcytlgfepejsou'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'mtanswsdrbyvdqnomukv'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'wjmhyhyzzbcjaabhahmy'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(82.71720813915931)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'nifspjhrgulqkzvgjryr'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ppgszmbxzgehsughgtdd', 'okzcpcwhyeyrwgcghzeo', 'kllqspsmhzdbpzixqsns']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'jbckyrdqelbrhliokpil'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'zfannvbcytlgfepejsou'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
