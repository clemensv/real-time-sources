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
            site_no='byhnhgcbuujrwzlxmqws',
            datetime='dxiwftihopampvkvycdp',
            value=float(71.81153557820198),
            exception='tztrsurdggzavavqqgil',
            qualifiers=['mhlsocqpymqucqfpwnoo', 'zrzznvtsgxvejmhzqxpt'],
            parameter_cd='xagkvwrzykqxacrxcrid',
            timeseries_cd='zcvviwnxwbumuzaxngae'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'byhnhgcbuujrwzlxmqws'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'dxiwftihopampvkvycdp'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(71.81153557820198)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'tztrsurdggzavavqqgil'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['mhlsocqpymqucqfpwnoo', 'zrzznvtsgxvejmhzqxpt']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'xagkvwrzykqxacrxcrid'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'zcvviwnxwbumuzaxngae'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
