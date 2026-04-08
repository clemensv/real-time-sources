"""
Test case for Measurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from luchtmeetnet_nl_producer_data.nl.rivm.luchtmeetnet.measurement import Measurement


class Test_Measurement(unittest.TestCase):
    """
    Test case for Measurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Measurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Measurement for testing
        """
        instance = Measurement(
            station_number='kuebykpkmacyjmomxffw',
            formula='wdelooueqjqletsulkrm',
            value=float(20.9104662074856),
            timestamp_measured='xklrrieqllpsjkmmagwl'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'kuebykpkmacyjmomxffw'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_formula_property(self):
        """
        Test formula property
        """
        test_value = 'wdelooueqjqletsulkrm'
        self.instance.formula = test_value
        self.assertEqual(self.instance.formula, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(20.9104662074856)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_timestamp_measured_property(self):
        """
        Test timestamp_measured property
        """
        test_value = 'xklrrieqllpsjkmmagwl'
        self.instance.timestamp_measured = test_value
        self.assertEqual(self.instance.timestamp_measured, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Measurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
