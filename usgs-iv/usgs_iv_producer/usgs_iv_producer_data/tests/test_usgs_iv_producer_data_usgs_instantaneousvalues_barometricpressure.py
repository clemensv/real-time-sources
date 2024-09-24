"""
Test case for BarometricPressure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.barometricpressure import BarometricPressure


class Test_BarometricPressure(unittest.TestCase):
    """
    Test case for BarometricPressure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BarometricPressure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BarometricPressure for testing
        """
        instance = BarometricPressure(
            site_no='mmgqwnvpwwejrjertbwk',
            datetime='vpewyigtcdiajarmpzlz',
            value=float(38.377620994374425),
            exception='yhpykvcpdvmczlmmgttr',
            qualifiers=['rulmscaysjvkusngenqh'],
            parameter_cd='shkdkkzxclmkelyyoptw',
            timeseries_cd='ygbetplnxlobveinzgon'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'mmgqwnvpwwejrjertbwk'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'vpewyigtcdiajarmpzlz'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(38.377620994374425)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'yhpykvcpdvmczlmmgttr'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['rulmscaysjvkusngenqh']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'shkdkkzxclmkelyyoptw'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ygbetplnxlobveinzgon'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
