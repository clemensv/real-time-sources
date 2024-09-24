"""
Test case for PH
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.ph import PH


class Test_PH(unittest.TestCase):
    """
    Test case for PH
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PH.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PH for testing
        """
        instance = PH(
            site_no='jvwxxxefquebkeqngvzy',
            datetime='csrghodvothwlogpefdo',
            value=float(58.19651612738345),
            exception='tklrxoqmjayttmmvjatq',
            qualifiers=['eanaobevnoqzowzybymo', 'rxdnkabspgacrovnzwjb', 'sfciwgnmzkhbbpujihzi'],
            parameter_cd='cjjnrhkolgvuppykrvxu',
            timeseries_cd='kermrqsyahnmolagsvdu'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'jvwxxxefquebkeqngvzy'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'csrghodvothwlogpefdo'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(58.19651612738345)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'tklrxoqmjayttmmvjatq'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['eanaobevnoqzowzybymo', 'rxdnkabspgacrovnzwjb', 'sfciwgnmzkhbbpujihzi']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'cjjnrhkolgvuppykrvxu'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'kermrqsyahnmolagsvdu'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
