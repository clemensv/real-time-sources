"""
Test case for StopTimeUpdate
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate import StopTimeUpdate
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeevent import StopTimeEvent
from typing import Any


class Test_StopTimeUpdate(unittest.TestCase):
    """
    Test case for StopTimeUpdate
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StopTimeUpdate.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StopTimeUpdate for testing
        """
        instance = StopTimeUpdate(
            stop_sequence=int(8),
            stop_id='ukcnratxfiduqgenwxue',
            arrival=None,
            departure=None,
            schedule_relationship=None
        )
        return instance

    
    def test_stop_sequence_property(self):
        """
        Test stop_sequence property
        """
        test_value = int(8)
        self.instance.stop_sequence = test_value
        self.assertEqual(self.instance.stop_sequence, test_value)
    
    def test_stop_id_property(self):
        """
        Test stop_id property
        """
        test_value = 'ukcnratxfiduqgenwxue'
        self.instance.stop_id = test_value
        self.assertEqual(self.instance.stop_id, test_value)
    
    def test_arrival_property(self):
        """
        Test arrival property
        """
        test_value = None
        self.instance.arrival = test_value
        self.assertEqual(self.instance.arrival, test_value)
    
    def test_departure_property(self):
        """
        Test departure property
        """
        test_value = None
        self.instance.departure = test_value
        self.assertEqual(self.instance.departure, test_value)
    
    def test_schedule_relationship_property(self):
        """
        Test schedule_relationship property
        """
        test_value = None
        self.instance.schedule_relationship = test_value
        self.assertEqual(self.instance.schedule_relationship, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StopTimeUpdate.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StopTimeUpdate.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

