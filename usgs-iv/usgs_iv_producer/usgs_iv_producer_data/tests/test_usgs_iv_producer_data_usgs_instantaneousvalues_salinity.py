"""
Test case for Salinity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.salinity import Salinity


class Test_Salinity(unittest.TestCase):
    """
    Test case for Salinity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Salinity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Salinity for testing
        """
        instance = Salinity(
            site_no='uvudquwhavorbhgtlyxc',
            datetime='wijxknmtmegxjevpfjbk',
            value=float(51.413181272733254),
            exception='adelrtdkmzkhbojtjqya',
            qualifiers=['asidsauegjqnhvjdpldc', 'evtyrfioeqmxctjnfuix', 'kruhktedhlkktcwyvbil', 'qlunyoefeakvwjbbxaok'],
            parameter_cd='jnbesqroaagzalbqbvcf',
            timeseries_cd='clxtfznoirkqesaqvoqu'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'uvudquwhavorbhgtlyxc'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'wijxknmtmegxjevpfjbk'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(51.413181272733254)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'adelrtdkmzkhbojtjqya'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['asidsauegjqnhvjdpldc', 'evtyrfioeqmxctjnfuix', 'kruhktedhlkktcwyvbil', 'qlunyoefeakvwjbbxaok']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'jnbesqroaagzalbqbvcf'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'clxtfznoirkqesaqvoqu'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
