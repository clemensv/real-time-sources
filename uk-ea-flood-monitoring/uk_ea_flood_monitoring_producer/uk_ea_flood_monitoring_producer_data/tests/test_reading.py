"""
Test case for Reading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uk_ea_flood_monitoring_producer_data.reading import Reading
import datetime


class Test_Reading(unittest.TestCase):
    """
    Test case for Reading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Reading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Reading for testing
        """
        instance = Reading(
            station_reference='otxuwmjwzmkzpqoefcqs',
            date_time=datetime.datetime.now(datetime.timezone.utc),
            measure='crhqhnxgjbzypkptwwrk',
            value=float(96.5254097356516)
        )
        return instance

    
    def test_station_reference_property(self):
        """
        Test station_reference property
        """
        test_value = 'otxuwmjwzmkzpqoefcqs'
        self.instance.station_reference = test_value
        self.assertEqual(self.instance.station_reference, test_value)
    
    def test_date_time_property(self):
        """
        Test date_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_time = test_value
        self.assertEqual(self.instance.date_time, test_value)
    
    def test_measure_property(self):
        """
        Test measure property
        """
        test_value = 'crhqhnxgjbzypkptwwrk'
        self.instance.measure = test_value
        self.assertEqual(self.instance.measure, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(96.5254097356516)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Reading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Reading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

