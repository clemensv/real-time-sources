"""
Test case for FDOM
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.fdom import FDOM


class Test_FDOM(unittest.TestCase):
    """
    Test case for FDOM
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FDOM.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FDOM for testing
        """
        instance = FDOM(
            site_no='yhghhvqqwoveuophpltg',
            datetime='kfnzytayakggfkvflgxi',
            value=float(9.582062141455317),
            exception='gdglwaoluudttbnupgba',
            qualifiers=['zjealbymfiocdoikgsre', 'lhpkokihhhxqxemrojvj'],
            parameter_cd='vgguoszivgyssseqthgl',
            timeseries_cd='hktmnuyiziawnylszvsd'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'yhghhvqqwoveuophpltg'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'kfnzytayakggfkvflgxi'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(9.582062141455317)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'gdglwaoluudttbnupgba'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['zjealbymfiocdoikgsre', 'lhpkokihhhxqxemrojvj']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'vgguoszivgyssseqthgl'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'hktmnuyiziawnylszvsd'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
