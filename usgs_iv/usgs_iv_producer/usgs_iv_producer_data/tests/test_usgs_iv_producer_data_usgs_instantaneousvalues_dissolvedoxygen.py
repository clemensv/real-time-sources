"""
Test case for DissolvedOxygen
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.dissolvedoxygen import DissolvedOxygen


class Test_DissolvedOxygen(unittest.TestCase):
    """
    Test case for DissolvedOxygen
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DissolvedOxygen.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DissolvedOxygen for testing
        """
        instance = DissolvedOxygen(
            site_no='xchjehawoqnvmxdblqsa',
            datetime='ppjoawcsjxrehbqkejjr',
            value=float(30.938445102492473),
            qualifiers=['kjaerarmlszlqanqxwnz', 'jeeioofgbonfzblyanec'],
            parameter_cd='dosdokmsuwbxlssuywmm',
            timeseries_cd='tmfiuvicaywiegnpypri'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'xchjehawoqnvmxdblqsa'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'ppjoawcsjxrehbqkejjr'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(30.938445102492473)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['kjaerarmlszlqanqxwnz', 'jeeioofgbonfzblyanec']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'dosdokmsuwbxlssuywmm'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'tmfiuvicaywiegnpypri'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
