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
            site_no='vryghtxwlcarzolyimjp',
            datetime='dvrwynmzxfgrkrgurgzk',
            value=float(94.15271002341554),
            exception='gjhqjqposwfnkrvpqyun',
            qualifiers=['bvynlvihpoydveyeitan', 'ilosjcmqxoqqayvctgbn', 'futiddasjznxmjmvwwtn', 'ulxgopariwlvdsbklieb'],
            parameter_cd='ndwoekxorsotdthqypoz',
            timeseries_cd='enqjsdgimgrgcynrdgoq'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'vryghtxwlcarzolyimjp'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'dvrwynmzxfgrkrgurgzk'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(94.15271002341554)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'gjhqjqposwfnkrvpqyun'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['bvynlvihpoydveyeitan', 'ilosjcmqxoqqayvctgbn', 'futiddasjznxmjmvwwtn', 'ulxgopariwlvdsbklieb']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'ndwoekxorsotdthqypoz'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'enqjsdgimgrgcynrdgoq'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
