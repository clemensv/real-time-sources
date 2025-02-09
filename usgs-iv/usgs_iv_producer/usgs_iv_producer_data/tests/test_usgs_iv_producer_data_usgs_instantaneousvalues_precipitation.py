"""
Test case for Precipitation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.precipitation import Precipitation


class Test_Precipitation(unittest.TestCase):
    """
    Test case for Precipitation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Precipitation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Precipitation for testing
        """
        instance = Precipitation(
            site_no='rrnpjpnmbdnvfkspturw',
            datetime='zhmlwpzvtwubdmpkklaa',
            value=float(6.8284899627710445),
            exception='uixusdavarjbvtdysyhh',
            qualifiers=['srkxdctoaozkiwhyouwn'],
            parameter_cd='iodrbssivjmutwkscpjn',
            timeseries_cd='kusqlmosuoifmcsggdeu'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'rrnpjpnmbdnvfkspturw'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'zhmlwpzvtwubdmpkklaa'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(6.8284899627710445)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'uixusdavarjbvtdysyhh'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['srkxdctoaozkiwhyouwn']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'iodrbssivjmutwkscpjn'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'kusqlmosuoifmcsggdeu'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
