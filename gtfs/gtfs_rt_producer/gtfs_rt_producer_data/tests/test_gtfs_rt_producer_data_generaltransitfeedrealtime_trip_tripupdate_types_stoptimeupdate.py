"""
Test case for StopTimeUpdate
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate import StopTimeUpdate
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_trip_tripupdate_types_stoptimeevent import Test_StopTimeEvent
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_trip_tripupdate_types_stoptimeupdate_types_schedulerelationship import Test_ScheduleRelationship

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
            stop_sequence=int(77),
            stop_id='mhadwyaehvdwpunlecmj',
            arrival=Test_StopTimeEvent.create_instance(),
            departure=Test_StopTimeEvent.create_instance(),
            schedule_relationship=Test_ScheduleRelationship.create_instance()
        )
        return instance

    
    def test_stop_sequence_property(self):
        """
        Test stop_sequence property
        """
        test_value = int(77)
        self.instance.stop_sequence = test_value
        self.assertEqual(self.instance.stop_sequence, test_value)
    
    def test_stop_id_property(self):
        """
        Test stop_id property
        """
        test_value = 'mhadwyaehvdwpunlecmj'
        self.instance.stop_id = test_value
        self.assertEqual(self.instance.stop_id, test_value)
    
    def test_arrival_property(self):
        """
        Test arrival property
        """
        test_value = Test_StopTimeEvent.create_instance()
        self.instance.arrival = test_value
        self.assertEqual(self.instance.arrival, test_value)
    
    def test_departure_property(self):
        """
        Test departure property
        """
        test_value = Test_StopTimeEvent.create_instance()
        self.instance.departure = test_value
        self.assertEqual(self.instance.departure, test_value)
    
    def test_schedule_relationship_property(self):
        """
        Test schedule_relationship property
        """
        test_value = Test_ScheduleRelationship.create_instance()
        self.instance.schedule_relationship = test_value
        self.assertEqual(self.instance.schedule_relationship, test_value)
    
