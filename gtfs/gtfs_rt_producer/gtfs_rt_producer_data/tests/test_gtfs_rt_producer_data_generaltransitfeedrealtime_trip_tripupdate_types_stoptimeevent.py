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
            delay=int(62),
            time=int(97),
            uncertainty=int(12)
        )
        return instance

    
    def test_delay_property(self):
        """
        Test delay property
        """
        test_value = int(62)
        self.instance.delay = test_value
        self.assertEqual(self.instance.delay, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(97)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_uncertainty_property(self):
        """
        Test uncertainty property
        """
        test_value = int(12)
        self.instance.uncertainty = test_value
        self.assertEqual(self.instance.uncertainty, test_value)
    
