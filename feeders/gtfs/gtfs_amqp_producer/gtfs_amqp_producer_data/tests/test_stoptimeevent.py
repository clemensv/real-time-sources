"""
Test case for StopTimeEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeevent import StopTimeEvent


class Test_StopTimeEvent(unittest.TestCase):
    """
    Test case for StopTimeEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StopTimeEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StopTimeEvent for testing
        """
        instance = StopTimeEvent(
            delay=int(51),
            time=int(96),
            uncertainty=int(91)
        )
        return instance

    
    def test_delay_property(self):
        """
        Test delay property
        """
        test_value = int(51)
        self.instance.delay = test_value
        self.assertEqual(self.instance.delay, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(96)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_uncertainty_property(self):
        """
        Test uncertainty property
        """
        test_value = int(91)
        self.instance.uncertainty = test_value
        self.assertEqual(self.instance.uncertainty, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StopTimeEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StopTimeEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

