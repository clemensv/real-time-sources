"""
Test case for OtherParameter
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.otherparameter import OtherParameter


class Test_OtherParameter(unittest.TestCase):
    """
    Test case for OtherParameter
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_OtherParameter.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OtherParameter for testing
        """
        instance = OtherParameter(
            site_no='hhyvsagvhrxiwimmipdq',
            datetime='jczscwxqihfisunnqzlv',
            value=float(70.1415000179727),
            exception='srdwscauqmrbhqkxqodp',
            qualifiers=['bncpnvzvaypntcfxqljl', 'ilmfddhbqovxnmssahda'],
            parameter_cd='rhvuptghgohrnzpwxmlr',
            timeseries_cd='vstzifujexndpehdqdou'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'hhyvsagvhrxiwimmipdq'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'jczscwxqihfisunnqzlv'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(70.1415000179727)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'srdwscauqmrbhqkxqodp'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['bncpnvzvaypntcfxqljl', 'ilmfddhbqovxnmssahda']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'rhvuptghgohrnzpwxmlr'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'vstzifujexndpehdqdou'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = OtherParameter.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
