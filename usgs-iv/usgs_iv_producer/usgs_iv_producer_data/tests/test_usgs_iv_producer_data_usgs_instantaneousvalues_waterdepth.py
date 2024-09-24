"""
Test case for WaterDepth
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.waterdepth import WaterDepth


class Test_WaterDepth(unittest.TestCase):
    """
    Test case for WaterDepth
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterDepth.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterDepth for testing
        """
        instance = WaterDepth(
            site_no='aovhwgudcgtfimbgtnqa',
            datetime='hqytuviqroicagxyyrmm',
            value=float(4.492804932488015),
            exception='ljnveltnrtygebkzeiml',
            qualifiers=['rkddrxtvvlxqlrypnczy', 'zeutpbbrjchtzybzytkz', 'uiymhoyczprdxrukiusv', 'gwkjyjtxgnvfnagrzcsl', 'rcettinsilonwkotooxy'],
            parameter_cd='qgzfnnjdwafhkvqupsyb',
            timeseries_cd='ymyqangeuqzovxxzkwif'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'aovhwgudcgtfimbgtnqa'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'hqytuviqroicagxyyrmm'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(4.492804932488015)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'ljnveltnrtygebkzeiml'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['rkddrxtvvlxqlrypnczy', 'zeutpbbrjchtzybzytkz', 'uiymhoyczprdxrukiusv', 'gwkjyjtxgnvfnagrzcsl', 'rcettinsilonwkotooxy']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'qgzfnnjdwafhkvqupsyb'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ymyqangeuqzovxxzkwif'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
