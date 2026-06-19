"""
Test case for Predictions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_amqp_producer_data.microsoft.opendata.us.noaa.predictions import Predictions


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
            station_id='nmywuhnxngqumkihsyjq',
            timestamp='ddnmcjyztlfyhvimbbyn',
            value=float(5.005067363692994),
            region='xlymosmbxxwehweocaqj'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nmywuhnxngqumkihsyjq'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'ddnmcjyztlfyhvimbbyn'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(5.005067363692994)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'xlymosmbxxwehweocaqj'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Predictions.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Predictions.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

