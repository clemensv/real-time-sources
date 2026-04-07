"""
Test case for Predictions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.predictions import Predictions


class Test_Predictions(unittest.TestCase):
    """
    Test case for Predictions
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Predictions.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Predictions for testing
        """
        instance = Predictions(
            station_id='qyapnfpbzbpxyiabjxba',
            timestamp='ytwqugrenwiltuyzukek',
            value=float(89.993330317572)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'qyapnfpbzbpxyiabjxba'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'ytwqugrenwiltuyzukek'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(89.993330317572)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Predictions.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
