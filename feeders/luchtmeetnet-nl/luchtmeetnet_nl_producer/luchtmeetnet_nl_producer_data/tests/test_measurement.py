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
            station_number='shewgsqbxuvvxjiojuxw',
            formula='padqbkdgnmcuqnkdfhyg',
            value=float(53.427991317215394),
            timestamp_measured='ekdptperhelgdlyegbou'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'shewgsqbxuvvxjiojuxw'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_formula_property(self):
        """
        Test formula property
        """
        test_value = 'padqbkdgnmcuqnkdfhyg'
        self.instance.formula = test_value
        self.assertEqual(self.instance.formula, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(53.427991317215394)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_timestamp_measured_property(self):
        """
        Test timestamp_measured property
        """
        test_value = 'ekdptperhelgdlyegbou'
        self.instance.timestamp_measured = test_value
        self.assertEqual(self.instance.timestamp_measured, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Measurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Measurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

