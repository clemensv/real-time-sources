"""
Test case for OtherParameter
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.otherparameter import OtherParameter


class Test_OtherParameter(unittest.TestCase):
    """
    Test case for OtherParameter
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_OtherParameter.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OtherParameter for testing
        """
        instance = OtherParameter(
            site_no='hzaagzpdpdzrjdawxvzj',
            datetime='dsjiempyubhfvkeanpjb',
            value=float(21.586007156679145),
            exception='iaxqnwnsmaxesswswtvj',
            qualifiers=['oqhyaayvnukagnezsasj'],
            parameter_cd='gmfewqzlpyrhdtbzphvs',
            timeseries_cd='vvxzgbrjgyxwkcscxyvz'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'hzaagzpdpdzrjdawxvzj'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'dsjiempyubhfvkeanpjb'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(21.586007156679145)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'iaxqnwnsmaxesswswtvj'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['oqhyaayvnukagnezsasj']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'gmfewqzlpyrhdtbzphvs'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'vvxzgbrjgyxwkcscxyvz'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
