"""
Test case for TurbidityFNU
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs-iv-producer_data.usgs.instantaneousvalues.turbidityfnu import TurbidityFNU


class Test_TurbidityFNU(unittest.TestCase):
    """
    Test case for TurbidityFNU
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TurbidityFNU.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TurbidityFNU for testing
        """
        instance = TurbidityFNU(
            site_no='yctdwckxssjwtfvskfij',
            datetime='gfblgybwvxhyxniymfvj',
            value=float(41.17846916817921),
            exception='kmqcfajcjmxeawasgfci',
            qualifiers=['ecwgqakytufmchcxgwef', 'tmvszdmnylnjvmcxtvtx'],
            parameter_cd='ewhflifxnyrkmjziravh',
            timeseries_cd='zrvykykkromuosezfyxn'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'yctdwckxssjwtfvskfij'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'gfblgybwvxhyxniymfvj'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(41.17846916817921)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'kmqcfajcjmxeawasgfci'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ecwgqakytufmchcxgwef', 'tmvszdmnylnjvmcxtvtx']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'ewhflifxnyrkmjziravh'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'zrvykykkromuosezfyxn'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TurbidityFNU.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
