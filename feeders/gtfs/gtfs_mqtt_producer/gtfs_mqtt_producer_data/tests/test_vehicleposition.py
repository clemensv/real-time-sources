"""
Test case for VehiclePosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition import VehiclePosition
from typing import Any
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.vehicle.vehicledescriptor import VehicleDescriptor
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.vehicle.position import Position
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.vehicle.tripdescriptor import TripDescriptor


class Test_VehiclePosition(unittest.TestCase):
    """
    Test case for VehiclePosition
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VehiclePosition.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VehiclePosition for testing
        """
        instance = VehiclePosition(
            trip=None,
            vehicle=None,
            position=None,
            current_stop_sequence=int(84),
            stop_id='hawrrnlsuyjkjtddbduc',
            current_status=None,
            timestamp=int(47),
            congestion_level=None,
            occupancy_status=None
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
    
    def test_position_property(self):
        """
        Test position property
        """
        test_value = None
        self.instance.position = test_value
        self.assertEqual(self.instance.position, test_value)
    
    def test_current_stop_sequence_property(self):
        """
        Test current_stop_sequence property
        """
        test_value = int(84)
        self.instance.current_stop_sequence = test_value
        self.assertEqual(self.instance.current_stop_sequence, test_value)
    
    def test_stop_id_property(self):
        """
        Test stop_id property
        """
        test_value = 'hawrrnlsuyjkjtddbduc'
        self.instance.stop_id = test_value
        self.assertEqual(self.instance.stop_id, test_value)
    
    def test_current_status_property(self):
        """
        Test current_status property
        """
        test_value = None
        self.instance.current_status = test_value
        self.assertEqual(self.instance.current_status, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(47)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_congestion_level_property(self):
        """
        Test congestion_level property
        """
        test_value = None
        self.instance.congestion_level = test_value
        self.assertEqual(self.instance.congestion_level, test_value)
    
    def test_occupancy_status_property(self):
        """
        Test occupancy_status property
        """
        test_value = None
        self.instance.occupancy_status = test_value
        self.assertEqual(self.instance.occupancy_status, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VehiclePosition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VehiclePosition.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

