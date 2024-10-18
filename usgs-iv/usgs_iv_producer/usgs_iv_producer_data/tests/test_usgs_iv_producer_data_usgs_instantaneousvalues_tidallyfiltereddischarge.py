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
            site_no='eqhdvfjdnvmnovmqiwlh',
            datetime='ithqmlrlioljufnyetys',
            value=float(43.1597307655756),
            exception='zelguiakceztcruiroya',
            qualifiers=['cegdqkrcggluvrtiwbyv', 'vggyusgxgxoqvwfxaydv', 'shxflpikhtvirvqlpysn', 'pgsvkrftwhpmeypipbut', 'cebltkescneopcslivsk'],
            parameter_cd='rsurpbxxizhogiajrjve',
            timeseries_cd='jgtenzcbuaktdnqobdck'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'eqhdvfjdnvmnovmqiwlh'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'ithqmlrlioljufnyetys'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(43.1597307655756)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'zelguiakceztcruiroya'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['cegdqkrcggluvrtiwbyv', 'vggyusgxgxoqvwfxaydv', 'shxflpikhtvirvqlpysn', 'pgsvkrftwhpmeypipbut', 'cebltkescneopcslivsk']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'rsurpbxxizhogiajrjve'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'jgtenzcbuaktdnqobdck'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
