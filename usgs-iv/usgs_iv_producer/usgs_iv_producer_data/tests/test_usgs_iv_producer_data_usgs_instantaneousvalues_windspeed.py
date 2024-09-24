"""
Test case for WindSpeed
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.windspeed import WindSpeed


class Test_WindSpeed(unittest.TestCase):
    """
    Test case for WindSpeed
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WindSpeed.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WindSpeed for testing
        """
        instance = WindSpeed(
            site_no='rmyxjwwhrbksxkvvtyjc',
            datetime='nvplxewhzgztdepygrlz',
            value=float(86.10151561771076),
            exception='rtubnqjnfysptxcmqqhm',
            qualifiers=['mscnlbrsuwcoetamaxbd', 'zinzvteqoeordxnidrkz'],
            parameter_cd='iifobhorlacnlsqondzd',
            timeseries_cd='godptcobamqfpgbgdcbt'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'rmyxjwwhrbksxkvvtyjc'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'nvplxewhzgztdepygrlz'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(86.10151561771076)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'rtubnqjnfysptxcmqqhm'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['mscnlbrsuwcoetamaxbd', 'zinzvteqoeordxnidrkz']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'iifobhorlacnlsqondzd'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'godptcobamqfpgbgdcbt'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
