"""
Test case for StopTimeEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeevent import StopTimeEvent


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
            delay=int(16),
            time=int(80),
            uncertainty=int(24)
        )
        return instance

    
    def test_delay_property(self):
        """
        Test delay property
        """
        test_value = int(16)
        self.instance.delay = test_value
        self.assertEqual(self.instance.delay, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(80)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_uncertainty_property(self):
        """
        Test uncertainty property
        """
        test_value = int(24)
        self.instance.uncertainty = test_value
        self.assertEqual(self.instance.uncertainty, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StopTimeEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
