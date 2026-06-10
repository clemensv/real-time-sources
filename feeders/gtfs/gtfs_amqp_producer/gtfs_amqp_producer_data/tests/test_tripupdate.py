"""
Test case for TripUpdate
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.trip.tripupdate import TripUpdate
from gtfs_amqp_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate import StopTimeUpdate
from gtfs_amqp_producer_data.generaltransitfeedrealtime.trip.vehicledescriptor import VehicleDescriptor
from gtfs_amqp_producer_data.generaltransitfeedrealtime.trip.tripdescriptor import TripDescriptor


class Test_TripUpdate(unittest.TestCase):
    """
    Test case for TripUpdate
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TripUpdate.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TripUpdate for testing
        """
        instance = TripUpdate(
            trip=None,
            vehicle=None,
            stop_time_update=[None, None],
            timestamp=int(20),
            delay=int(62)
        )
        return instance

    
    def test_trip_property(self):
        """
        Test trip property
        """
        test_value = None
        self.instance.trip = test_value
        self.assertEqual(self.instance.trip, test_value)
    
    def test_vehicle_property(self):
        """
        Test vehicle property
        """
        test_value = None
        self.instance.vehicle = test_value
        self.assertEqual(self.instance.vehicle, test_value)
    
    def test_stop_time_update_property(self):
        """
        Test stop_time_update property
        """
        test_value = [None, None]
        self.instance.stop_time_update = test_value
        self.assertEqual(self.instance.stop_time_update, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(20)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_delay_property(self):
        """
        Test delay property
        """
        test_value = int(62)
        self.instance.delay = test_value
        self.assertEqual(self.instance.delay, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TripUpdate.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TripUpdate.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

