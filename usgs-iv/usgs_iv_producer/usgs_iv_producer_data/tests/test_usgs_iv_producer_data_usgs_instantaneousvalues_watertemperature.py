"""
Test case for WaterTemperature
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.watertemperature import WaterTemperature


class Test_WaterTemperature(unittest.TestCase):
    """
    Test case for WaterTemperature
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterTemperature.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterTemperature for testing
        """
        instance = WaterTemperature(
            site_no='vhlgioaxbqwbtvpezxcq',
            datetime='eksracthyqgkgooxvlnl',
            value=float(1.2413211925511702),
            exception='yyrvybvuslzzsgmteytq',
            qualifiers=['jcykubtbxzonowkssodr', 'bgzhxioukshxtdiavahp'],
            parameter_cd='wyyiiveanaghnrkwezbu',
            timeseries_cd='hadsfxjoradreklcupes'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'vhlgioaxbqwbtvpezxcq'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'eksracthyqgkgooxvlnl'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(1.2413211925511702)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'yyrvybvuslzzsgmteytq'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['jcykubtbxzonowkssodr', 'bgzhxioukshxtdiavahp']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'wyyiiveanaghnrkwezbu'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'hadsfxjoradreklcupes'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
