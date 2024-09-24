"""
Test case for AirTemperature
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.airtemperature import AirTemperature


class Test_AirTemperature(unittest.TestCase):
    """
    Test case for AirTemperature
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AirTemperature.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AirTemperature for testing
        """
        instance = AirTemperature(
            site_no='ikjdiboeyleifkpbkdos',
            datetime='ytadiztrhoiqnngszwzm',
            value=float(50.33646160384176),
            exception='dfeurbloyfuocwdwuavl',
            qualifiers=['mjkejuplvqohgiksalcw', 'ktsyqrrvurcgzriwgbem', 'nxglkhlqjqajzzvzyked', 'qkmfykilgtoitrnhbugj', 'nolzfmkonvkwikhkurlb'],
            parameter_cd='udmztrisannttokdlhle',
            timeseries_cd='ezwwgygzkbuzdhnebnqo'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'ikjdiboeyleifkpbkdos'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'ytadiztrhoiqnngszwzm'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(50.33646160384176)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'dfeurbloyfuocwdwuavl'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['mjkejuplvqohgiksalcw', 'ktsyqrrvurcgzriwgbem', 'nxglkhlqjqajzzvzyked', 'qkmfykilgtoitrnhbugj', 'nolzfmkonvkwikhkurlb']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'udmztrisannttokdlhle'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ezwwgygzkbuzdhnebnqo'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
