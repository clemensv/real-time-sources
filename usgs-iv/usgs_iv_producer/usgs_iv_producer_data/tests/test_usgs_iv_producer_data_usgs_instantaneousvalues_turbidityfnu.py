"""
Test case for TurbidityFNU
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.turbidityfnu import TurbidityFNU


class Test_TurbidityFNU(unittest.TestCase):
    """
    Test case for TurbidityFNU
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TurbidityFNU.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TurbidityFNU for testing
        """
        instance = TurbidityFNU(
            site_no='nnuviezrlqxubxllhrvx',
            datetime='qsmjyfeuriwqhcmdgfug',
            value=float(0.16859706706733313),
            exception='wofuzcqtnrcrtklarwjb',
            qualifiers=['kcrsqitkxwgksxzkfymw', 'jyfbkhansaiymnvsohjp', 'bwifdlntkfipbrolnnui'],
            parameter_cd='dbbbdfreqvijdlxfoblg',
            timeseries_cd='amibrhhqqoukdnvxuzcs'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'nnuviezrlqxubxllhrvx'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'qsmjyfeuriwqhcmdgfug'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(0.16859706706733313)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'wofuzcqtnrcrtklarwjb'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['kcrsqitkxwgksxzkfymw', 'jyfbkhansaiymnvsohjp', 'bwifdlntkfipbrolnnui']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'dbbbdfreqvijdlxfoblg'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'amibrhhqqoukdnvxuzcs'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
