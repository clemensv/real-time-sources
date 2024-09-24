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
            site_no='etdgwotxclupbpfrsnbh',
            datetime='ebjikcobfffaurbanwof',
            value=float(77.33832144237815),
            exception='wzkcpeezdcrzpvkfonrh',
            qualifiers=['ubykmnoadjoxwtceqahs', 'flcuqodvobxlhshhwkwh', 'hjasejcjsgbitthijdxb'],
            parameter_cd='khglwvcdvxcjjnichlbp',
            timeseries_cd='hgspeyshktgaboiunesy'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'etdgwotxclupbpfrsnbh'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'ebjikcobfffaurbanwof'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(77.33832144237815)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'wzkcpeezdcrzpvkfonrh'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ubykmnoadjoxwtceqahs', 'flcuqodvobxlhshhwkwh', 'hjasejcjsgbitthijdxb']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'khglwvcdvxcjjnichlbp'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'hgspeyshktgaboiunesy'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
