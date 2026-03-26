"""
Test case for Precipitation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.precipitation import Precipitation


class Test_Precipitation(unittest.TestCase):
    """
    Test case for Precipitation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Precipitation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Precipitation for testing
        """
        instance = Precipitation(
            site_no='gavaihgujhtbnpyscvoz',
            datetime='gazseocmecnvrjmrxsgn',
            value=float(15.176705207951525),
            exception='hdsuwsfvwhshcatwflkk',
            qualifiers=['sfqzcicmyashrjelauvz', 'tjxgjlmxiswybnxzzvwb'],
            parameter_cd='tgmucempaqkkumdvmczn',
            timeseries_cd='hfzioecimlcrmsbsptaq'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'gavaihgujhtbnpyscvoz'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'gazseocmecnvrjmrxsgn'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(15.176705207951525)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'hdsuwsfvwhshcatwflkk'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['sfqzcicmyashrjelauvz', 'tjxgjlmxiswybnxzzvwb']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'tgmucempaqkkumdvmczn'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'hfzioecimlcrmsbsptaq'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Precipitation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
