"""
Test case for SpecificConductance
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance


class Test_SpecificConductance(unittest.TestCase):
    """
    Test case for SpecificConductance
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SpecificConductance.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SpecificConductance for testing
        """
        instance = SpecificConductance(
            site_no='sdzuqpfxvnqleamnlstb',
            datetime='wjkuuxdihecjuqfvpkcq',
            value=float(10.429221317879023),
            exception='smvupbwpwreitegtxgms',
            qualifiers=['jlhunsaxmhvrkdfoohtd', 'gscejzqdqeiruwnovyvx', 'zymvnxwkyufreexdjlzd'],
            parameter_cd='rcvvytxbfytkkzgkryve',
            timeseries_cd='hudmtafmxmhgsoqdmozi'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'sdzuqpfxvnqleamnlstb'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'wjkuuxdihecjuqfvpkcq'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(10.429221317879023)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'smvupbwpwreitegtxgms'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['jlhunsaxmhvrkdfoohtd', 'gscejzqdqeiruwnovyvx', 'zymvnxwkyufreexdjlzd']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'rcvvytxbfytkkzgkryve'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'hudmtafmxmhgsoqdmozi'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
