"""
Test case for WindDirection
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.winddirection import WindDirection


class Test_WindDirection(unittest.TestCase):
    """
    Test case for WindDirection
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WindDirection.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WindDirection for testing
        """
        instance = WindDirection(
            site_no='zkagudcmubtqqwnziczy',
            datetime='lnjsjlenynxxrywbcpyq',
            value=float(11.793659927450884),
            exception='mgzlazxjqnhhgfdvjeea',
            qualifiers=['ynjumxijxqyexweifmmr', 'qmqowbbxnlgwpuvajpji'],
            parameter_cd='flyyamulttgyrwesvbgs',
            timeseries_cd='esbhwgvejolzupdfaxfp'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'zkagudcmubtqqwnziczy'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'lnjsjlenynxxrywbcpyq'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(11.793659927450884)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'mgzlazxjqnhhgfdvjeea'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ynjumxijxqyexweifmmr', 'qmqowbbxnlgwpuvajpji']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'flyyamulttgyrwesvbgs'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'esbhwgvejolzupdfaxfp'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
