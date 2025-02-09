"""
Test case for WindSpeed
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.windspeed import WindSpeed


class Test_WindSpeed(unittest.TestCase):
    """
    Test case for WindSpeed
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WindSpeed.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WindSpeed for testing
        """
        instance = WindSpeed(
            site_no='pbttbuxjlyxxcvlbemok',
            datetime='cytulrmbujazbtwgrbaa',
            value=float(87.34400177300266),
            exception='kpcxkivzjqrsflkypcsh',
            qualifiers=['gmumpszdgfhwlmlsqrqc'],
            parameter_cd='suqdqmkdmpjovsnhszhu',
            timeseries_cd='heaccechvhpqhwysulhs'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'pbttbuxjlyxxcvlbemok'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'cytulrmbujazbtwgrbaa'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(87.34400177300266)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'kpcxkivzjqrsflkypcsh'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['gmumpszdgfhwlmlsqrqc']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'suqdqmkdmpjovsnhszhu'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'heaccechvhpqhwysulhs'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
