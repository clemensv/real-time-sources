"""
Test case for PM25Reading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from singapore_nea_producer_data.pm25reading import PM25Reading
import datetime


class Test_PM25Reading(unittest.TestCase):
    """
    Test case for PM25Reading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PM25Reading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PM25Reading for testing
        """
        instance = PM25Reading(
            region='jdtmcokjzuodlfrhfdnc',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            update_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm25_one_hourly=int(7)
        )
        return instance

    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'jdtmcokjzuodlfrhfdnc'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_update_timestamp_property(self):
        """
        Test update_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.update_timestamp = test_value
        self.assertEqual(self.instance.update_timestamp, test_value)
    
    def test_pm25_one_hourly_property(self):
        """
        Test pm25_one_hourly property
        """
        test_value = int(7)
        self.instance.pm25_one_hourly = test_value
        self.assertEqual(self.instance.pm25_one_hourly, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PM25Reading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PM25Reading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

