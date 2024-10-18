"""
Test case for EstuaryElevationNGVD29
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.estuaryelevationngvd29 import EstuaryElevationNGVD29


class Test_EstuaryElevationNGVD29(unittest.TestCase):
    """
    Test case for EstuaryElevationNGVD29
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EstuaryElevationNGVD29.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EstuaryElevationNGVD29 for testing
        """
        instance = EstuaryElevationNGVD29(
            site_no='urbtukfkfekzxzrowybr',
            datetime='hfnjphjvyozeviztjyrw',
            value=float(44.032929973316406),
            exception='gsyfxhiybpuvccwpivrv',
            qualifiers=['mcfzwmqhbjgfsoplmflv'],
            parameter_cd='xpzvupmvfwfgyhclgmey',
            timeseries_cd='pnksmmemfksvujudcyfe'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'urbtukfkfekzxzrowybr'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'hfnjphjvyozeviztjyrw'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(44.032929973316406)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'gsyfxhiybpuvccwpivrv'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['mcfzwmqhbjgfsoplmflv']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'xpzvupmvfwfgyhclgmey'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'pnksmmemfksvujudcyfe'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
