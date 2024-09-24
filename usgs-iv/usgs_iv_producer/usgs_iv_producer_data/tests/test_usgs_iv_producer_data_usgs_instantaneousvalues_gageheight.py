"""
Test case for GageHeight
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.gageheight import GageHeight


class Test_GageHeight(unittest.TestCase):
    """
    Test case for GageHeight
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GageHeight.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GageHeight for testing
        """
        instance = GageHeight(
            site_no='nfryrnusxxbbygvsypbw',
            datetime='dnbsfrlkjcngcmioodbk',
            value=float(79.47522664063945),
            exception='ostwqklympsijfsiqfhk',
            qualifiers=['voptmucqrcpafjpvispz', 'ydzvrcenrrfuiqnucvps', 'bptrhypwntehrysensan', 'hwknighvqaagklkwwyxc', 'wkbdnqhhjvaqyfowstpx'],
            parameter_cd='phrrisgwyncuchohifrg',
            timeseries_cd='wgqujjrvuwspgubpqeke'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'nfryrnusxxbbygvsypbw'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'dnbsfrlkjcngcmioodbk'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(79.47522664063945)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'ostwqklympsijfsiqfhk'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['voptmucqrcpafjpvispz', 'ydzvrcenrrfuiqnucvps', 'bptrhypwntehrysensan', 'hwknighvqaagklkwwyxc', 'wkbdnqhhjvaqyfowstpx']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'phrrisgwyncuchohifrg'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'wgqujjrvuwspgubpqeke'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
