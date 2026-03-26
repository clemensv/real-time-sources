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
            site_no='fwymutzpxqdecknucbqa',
            datetime='damgquxkmgrdhxttfpfq',
            value=float(89.22195737918936),
            exception='fnvobictjvpswyzyithw',
            qualifiers=['pkwklrthhibrmpsxbznd', 'rfidjkambesuhlragjof'],
            parameter_cd='hdjcpryoloqhzdeumrvr',
            timeseries_cd='qmwjyyvkkclnhsgmiapw'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'fwymutzpxqdecknucbqa'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'damgquxkmgrdhxttfpfq'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(89.22195737918936)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'fnvobictjvpswyzyithw'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['pkwklrthhibrmpsxbznd', 'rfidjkambesuhlragjof']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'hdjcpryoloqhzdeumrvr'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'qmwjyyvkkclnhsgmiapw'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SpecificConductance.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
