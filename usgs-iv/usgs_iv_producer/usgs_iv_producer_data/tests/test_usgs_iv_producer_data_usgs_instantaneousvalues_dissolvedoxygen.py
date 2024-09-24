"""
Test case for DissolvedOxygen
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.dissolvedoxygen import DissolvedOxygen


class Test_DissolvedOxygen(unittest.TestCase):
    """
    Test case for DissolvedOxygen
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DissolvedOxygen.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DissolvedOxygen for testing
        """
        instance = DissolvedOxygen(
            site_no='lgimvbjediptmozusdag',
            datetime='jjwahyumwqspgyugkljc',
            value=float(93.4597324694838),
            exception='slwhoiyqielgsdkqldji',
            qualifiers=['tsipzmutqdojgtddnulx'],
            parameter_cd='frnuoidwcwmtmioooqdl',
            timeseries_cd='hnxhckcycshexleurfyd'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'lgimvbjediptmozusdag'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'jjwahyumwqspgyugkljc'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(93.4597324694838)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'slwhoiyqielgsdkqldji'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['tsipzmutqdojgtddnulx']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'frnuoidwcwmtmioooqdl'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'hnxhckcycshexleurfyd'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
