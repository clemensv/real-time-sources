"""
Test case for VehiclePosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicleposition import VehiclePosition
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_position import Test_Position
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_vehicleposition_types_congestionlevel import Test_CongestionLevel
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_vehicleposition_types_vehiclestopstatus import Test_VehicleStopStatus
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_vehicleposition_types_occupancystatus import Test_OccupancyStatus
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_vehicledescriptor import Test_VehicleDescriptor
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_tripdescriptor import Test_TripDescriptor

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
            trip=Test_TripDescriptor.create_instance(),
            vehicle=Test_VehicleDescriptor.create_instance(),
            position=Test_Position.create_instance(),
            current_stop_sequence=int(8),
            stop_id='uucysaakxenaefnrtbkc',
            current_status=Test_VehicleStopStatus.create_instance(),
            timestamp=int(61),
            congestion_level=Test_CongestionLevel.create_instance(),
            occupancy_status=Test_OccupancyStatus.create_instance()
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
    
    def test_position_property(self):
        """
        Test position property
        """
        test_value = Test_Position.create_instance()
        self.instance.position = test_value
        self.assertEqual(self.instance.position, test_value)
    
    def test_current_stop_sequence_property(self):
        """
        Test current_stop_sequence property
        """
        test_value = int(8)
        self.instance.current_stop_sequence = test_value
        self.assertEqual(self.instance.current_stop_sequence, test_value)
    
    def test_stop_id_property(self):
        """
        Test stop_id property
        """
        test_value = 'uucysaakxenaefnrtbkc'
        self.instance.stop_id = test_value
        self.assertEqual(self.instance.stop_id, test_value)
    
    def test_current_status_property(self):
        """
        Test current_status property
        """
        test_value = Test_VehicleStopStatus.create_instance()
        self.instance.current_status = test_value
        self.assertEqual(self.instance.current_status, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(61)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_congestion_level_property(self):
        """
        Test congestion_level property
        """
        test_value = Test_CongestionLevel.create_instance()
        self.instance.congestion_level = test_value
        self.assertEqual(self.instance.congestion_level, test_value)
    
    def test_occupancy_status_property(self):
        """
        Test occupancy_status property
        """
        test_value = Test_OccupancyStatus.create_instance()
        self.instance.occupancy_status = test_value
        self.assertEqual(self.instance.occupancy_status, test_value)
    
