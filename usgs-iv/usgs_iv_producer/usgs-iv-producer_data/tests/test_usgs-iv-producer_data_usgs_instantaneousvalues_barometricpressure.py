"""
Test case for BarometricPressure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs-iv-producer_data.usgs.instantaneousvalues.barometricpressure import BarometricPressure


class Test_BarometricPressure(unittest.TestCase):
    """
    Test case for BarometricPressure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BarometricPressure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BarometricPressure for testing
        """
        instance = BarometricPressure(
            site_no='qfqfnwargwkfbczpdgss',
            datetime='drorxdfzrtjepvdifuvj',
            value=float(11.560434680709164),
            exception='zwiorydvwcfylnzdkhtd',
            qualifiers=['qtuentbrfmkhzsjvmxwj', 'zwbjipxrfxvkhiagsycr'],
            parameter_cd='ekdkiwshbvdhdieqslyz',
            timeseries_cd='wcyfnllkwcscpztpyzab'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'qfqfnwargwkfbczpdgss'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'drorxdfzrtjepvdifuvj'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(11.560434680709164)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'zwiorydvwcfylnzdkhtd'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['qtuentbrfmkhzsjvmxwj', 'zwbjipxrfxvkhiagsycr']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'ekdkiwshbvdhdieqslyz'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'wcyfnllkwcscpztpyzab'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BarometricPressure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
