"""
Test case for CalendarDates
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.calendardates import CalendarDates
from typing import Any


class Test_CalendarDates(unittest.TestCase):
    """
    Test case for CalendarDates
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CalendarDates.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CalendarDates for testing
        """
        instance = CalendarDates(
            serviceId='khyehstdfolblaxzvgol',
            date='mnikexofmtexcwveqjvq',
            exceptionType=None
        )
        return instance

    
    def test_serviceId_property(self):
        """
        Test serviceId property
        """
        test_value = 'khyehstdfolblaxzvgol'
        self.instance.serviceId = test_value
        self.assertEqual(self.instance.serviceId, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'mnikexofmtexcwveqjvq'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_exceptionType_property(self):
        """
        Test exceptionType property
        """
        test_value = None
        self.instance.exceptionType = test_value
        self.assertEqual(self.instance.exceptionType, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CalendarDates.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CalendarDates.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

