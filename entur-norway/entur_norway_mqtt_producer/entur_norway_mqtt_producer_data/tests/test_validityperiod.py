"""
Test case for ValidityPeriod
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_mqtt_producer_data.no.entur.validityperiod import ValidityPeriod
import datetime


class Test_ValidityPeriod(unittest.TestCase):
    """
    Test case for ValidityPeriod
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ValidityPeriod.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ValidityPeriod for testing
        """
        instance = ValidityPeriod(
            start_time=datetime.datetime.now(datetime.timezone.utc),
            end_time=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ValidityPeriod.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ValidityPeriod.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

