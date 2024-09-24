"""
Test case for TidallyFilteredDischarge
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.tidallyfiltereddischarge import TidallyFilteredDischarge


class Test_TidallyFilteredDischarge(unittest.TestCase):
    """
    Test case for TidallyFilteredDischarge
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TidallyFilteredDischarge.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TidallyFilteredDischarge for testing
        """
        instance = TidallyFilteredDischarge(
            site_no='sjwjdrqdfqunmqencvjg',
            datetime='jchhkontkotghdvvamus',
            value=float(69.40858418081211),
            exception='pvjwhllcdaamzvqnivwa',
            qualifiers=['dtqkasttuuzwdwfoiomv'],
            parameter_cd='hwewpjxdgqblbxxwjdgl',
            timeseries_cd='jrhlnkgqpfelrkopmpel'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'sjwjdrqdfqunmqencvjg'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'jchhkontkotghdvvamus'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(69.40858418081211)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'pvjwhllcdaamzvqnivwa'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['dtqkasttuuzwdwfoiomv']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'hwewpjxdgqblbxxwjdgl'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'jrhlnkgqpfelrkopmpel'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
