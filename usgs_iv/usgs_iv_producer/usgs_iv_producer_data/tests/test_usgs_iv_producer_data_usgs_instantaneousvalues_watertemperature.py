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
            site_no='rdldkiymasdswghjggfn',
            datetime='turkmxooqpnxfvmxpddu',
            value=float(4.644631515219666),
            qualifiers=['jqvxccwzjbauifsmcsjo', 'ldmyafsllfolssqeqrsz']
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'rdldkiymasdswghjggfn'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'turkmxooqpnxfvmxpddu'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(4.644631515219666)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['jqvxccwzjbauifsmcsjo', 'ldmyafsllfolssqeqrsz']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
