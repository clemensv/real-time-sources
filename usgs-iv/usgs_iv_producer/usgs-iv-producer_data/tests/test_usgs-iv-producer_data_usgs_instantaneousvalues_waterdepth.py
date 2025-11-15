"""
Test case for WaterDepth
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs-iv-producer_data.usgs.instantaneousvalues.waterdepth import WaterDepth


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
            site_no='uvfigiqedxoakpvztuhr',
            datetime='vvbknpuwbalpkshlhxml',
            value=float(78.12816640311966),
            exception='ggfnlvgziiteydhuplwk',
            qualifiers=['egpkmgkmnxdservezjcv', 'opxkxdfkjbbbluxytycb', 'xsgajjorlzkpjqcythxn', 'gzdkabjyklnoqgfljkey', 'qzptpornqpppddmvekio'],
            parameter_cd='fmrwctqttzkumluuuuqj',
            timeseries_cd='ivkmulopovppfktvrszc'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'uvfigiqedxoakpvztuhr'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'vvbknpuwbalpkshlhxml'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(78.12816640311966)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'ggfnlvgziiteydhuplwk'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['egpkmgkmnxdservezjcv', 'opxkxdfkjbbbluxytycb', 'xsgajjorlzkpjqcythxn', 'gzdkabjyklnoqgfljkey', 'qzptpornqpppddmvekio']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'fmrwctqttzkumluuuuqj'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ivkmulopovppfktvrszc'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterDepth.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
