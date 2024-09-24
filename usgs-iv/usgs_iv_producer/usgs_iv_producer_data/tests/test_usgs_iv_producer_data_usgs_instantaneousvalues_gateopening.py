"""
Test case for GateOpening
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.gateopening import GateOpening


class Test_GateOpening(unittest.TestCase):
    """
    Test case for GateOpening
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GateOpening.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GateOpening for testing
        """
        instance = GateOpening(
            site_no='aujyaoozpgqujlpageui',
            datetime='ezwtrtouoxueacnxsnrv',
            value=float(3.6862315506607346),
            exception='iuaizjnentakgytyhmsb',
            qualifiers=['zphyyisbscqvnblhgsvg', 'yeozfexdwhpayegomfnl', 'acdrqyuuzngjaslutphi'],
            parameter_cd='yhuacdawovhegtsruwlr',
            timeseries_cd='pkamqqkwqvbuqkhzzwwn'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'aujyaoozpgqujlpageui'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'ezwtrtouoxueacnxsnrv'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(3.6862315506607346)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'iuaizjnentakgytyhmsb'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['zphyyisbscqvnblhgsvg', 'yeozfexdwhpayegomfnl', 'acdrqyuuzngjaslutphi']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'yhuacdawovhegtsruwlr'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'pkamqqkwqvbuqkhzzwwn'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    