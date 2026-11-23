"""
Test case for Threshold
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_mqtt_producer_data.usgs.waterdata.threshold import Threshold
from usgs_waterdata_mqtt_producer_data.usgs.waterdata.thresholdperiod import ThresholdPeriod


class Test_Threshold(unittest.TestCase):
    """
    Test case for Threshold
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Threshold.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Threshold for testing
        """
        instance = Threshold(
            name='fiskerxulreybkujzehz',
            type='zyszjhckrmmfwaxztdda',
            periods=[None, None, None, None, None],
            severity=int(84),
            description='idwwrgkxzkkfkvmvyvmk',
            display_color='egewfxhekvogilgoujin',
            reference_code='izdqkknieajbafqmesyi',
            processing_order='tbnrwcubenxlcbfugsyt'
        )
        return instance

    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'fiskerxulreybkujzehz'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'zyszjhckrmmfwaxztdda'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_periods_property(self):
        """
        Test periods property
        """
        test_value = [None, None, None, None, None]
        self.instance.periods = test_value
        self.assertEqual(self.instance.periods, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = int(84)
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'idwwrgkxzkkfkvmvyvmk'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_display_color_property(self):
        """
        Test display_color property
        """
        test_value = 'egewfxhekvogilgoujin'
        self.instance.display_color = test_value
        self.assertEqual(self.instance.display_color, test_value)
    
    def test_reference_code_property(self):
        """
        Test reference_code property
        """
        test_value = 'izdqkknieajbafqmesyi'
        self.instance.reference_code = test_value
        self.assertEqual(self.instance.reference_code, test_value)
    
    def test_processing_order_property(self):
        """
        Test processing_order property
        """
        test_value = 'tbnrwcubenxlcbfugsyt'
        self.instance.processing_order = test_value
        self.assertEqual(self.instance.processing_order, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Threshold.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Threshold.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

