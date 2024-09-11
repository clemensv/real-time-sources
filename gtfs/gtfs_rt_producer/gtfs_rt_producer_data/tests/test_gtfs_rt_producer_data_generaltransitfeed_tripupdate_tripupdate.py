"""
Test case for TripUpdate
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripupdate import TripUpdate
from test_gtfs_rt_producer_data_generaltransitfeed_tripupdate_tripupdate_types_stoptimeupdate import Test_StopTimeUpdate
from test_gtfs_rt_producer_data_generaltransitfeed_tripupdate_vehicledescriptor import Test_VehicleDescriptor
from test_gtfs_rt_producer_data_generaltransitfeed_tripupdate_tripdescriptor import Test_TripDescriptor

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
            trip=Test_TripDescriptor.create_instance(),
            vehicle=Test_VehicleDescriptor.create_instance(),
            stop_time_update=[Test_StopTimeUpdate.create_instance(), Test_StopTimeUpdate.create_instance(), Test_StopTimeUpdate.create_instance(), Test_StopTimeUpdate.create_instance()],
            timestamp=int(71),
            delay=int(84)
        )
        return instance

    
    def test_trip_property(self):
        """
        Test trip property
        """
        test_value = Test_TripDescriptor.create_instance()
        self.instance.trip = test_value
        self.assertEqual(self.instance.trip, test_value)
    
    def test_vehicle_property(self):
        """
        Test vehicle property
        """
        test_value = Test_VehicleDescriptor.create_instance()
        self.instance.vehicle = test_value
        self.assertEqual(self.instance.vehicle, test_value)
    
    def test_stop_time_update_property(self):
        """
        Test stop_time_update property
        """
        test_value = [Test_StopTimeUpdate.create_instance(), Test_StopTimeUpdate.create_instance(), Test_StopTimeUpdate.create_instance(), Test_StopTimeUpdate.create_instance()]
        self.instance.stop_time_update = test_value
        self.assertEqual(self.instance.stop_time_update, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(71)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_delay_property(self):
        """
        Test delay property
        """
        test_value = int(84)
        self.instance.delay = test_value
        self.assertEqual(self.instance.delay, test_value)
    