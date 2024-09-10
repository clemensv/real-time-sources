"""
Test case for FeedEntity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.feedentity import FeedEntity
from test_gtfs_rt_producer_data_generaltransitfeed_tripupdate import Test_TripUpdate
from test_gtfs_rt_producer_data_generaltransitfeed_vehicleposition import Test_VehiclePosition
from test_gtfs_rt_producer_data_generaltransitfeed_alert import Test_Alert

class Test_FeedEntity(unittest.TestCase):
    """
    Test case for FeedEntity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedEntity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedEntity for testing
        """
        instance = FeedEntity(
            id='apuqcwjklmzbmtmlyzsr',
            is_deleted=False,
            trip_update=Test_TripUpdate.create_instance(),
            vehicle=Test_VehiclePosition.create_instance(),
            alert=Test_Alert.create_instance()
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'apuqcwjklmzbmtmlyzsr'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_is_deleted_property(self):
        """
        Test is_deleted property
        """
        test_value = False
        self.instance.is_deleted = test_value
        self.assertEqual(self.instance.is_deleted, test_value)
    
    def test_trip_update_property(self):
        """
        Test trip_update property
        """
        test_value = Test_TripUpdate.create_instance()
        self.instance.trip_update = test_value
        self.assertEqual(self.instance.trip_update, test_value)
    
    def test_vehicle_property(self):
        """
        Test vehicle property
        """
        test_value = Test_VehiclePosition.create_instance()
        self.instance.vehicle = test_value
        self.assertEqual(self.instance.vehicle, test_value)
    
    def test_alert_property(self):
        """
        Test alert property
        """
        test_value = Test_Alert.create_instance()
        self.instance.alert = test_value
        self.assertEqual(self.instance.alert, test_value)
    
