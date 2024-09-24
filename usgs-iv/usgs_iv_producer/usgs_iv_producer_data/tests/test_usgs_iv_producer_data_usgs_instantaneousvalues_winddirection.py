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
            site_no='ibhextpcwejxmhilucrg',
            datetime='ofkuhrexpoibpbtrtaij',
            value=float(40.09300867252789),
            exception='furbdyycvkojstaqxutj',
            qualifiers=['fkkrunnyujvegktxmezw'],
            parameter_cd='fmtnimbdpjcyrbvsxiec',
            timeseries_cd='dnlcwahnhmdnoypsorwz'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'ibhextpcwejxmhilucrg'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'ofkuhrexpoibpbtrtaij'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(40.09300867252789)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'furbdyycvkojstaqxutj'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['fkkrunnyujvegktxmezw']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'fmtnimbdpjcyrbvsxiec'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'dnlcwahnhmdnoypsorwz'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
