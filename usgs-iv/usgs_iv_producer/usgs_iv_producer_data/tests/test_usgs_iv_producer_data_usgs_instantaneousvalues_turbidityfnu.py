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
            site_no='gxgkemtylxkhadatwanj',
            datetime='xhscwvvrtfkpddlnmcip',
            value=float(18.43517362627224),
            exception='gggsmtlrmpywvlkelyed',
            qualifiers=['ukdgnrcfeqpprquxdvwg', 'xryiqgogfpvfzlhoviff', 'krwfwbvpmpfflfyoyfph', 'qubzjpcuwrewhusicuhz'],
            parameter_cd='jglevquvmvuttinixbrb',
            timeseries_cd='slkqdtkinfmuifuozhff'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'gxgkemtylxkhadatwanj'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'xhscwvvrtfkpddlnmcip'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(18.43517362627224)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'gggsmtlrmpywvlkelyed'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ukdgnrcfeqpprquxdvwg', 'xryiqgogfpvfzlhoviff', 'krwfwbvpmpfflfyoyfph', 'qubzjpcuwrewhusicuhz']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'jglevquvmvuttinixbrb'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'slkqdtkinfmuifuozhff'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    