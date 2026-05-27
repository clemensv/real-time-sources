import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.occupancystatus import OccupancyStatus


class Test_OccupancyStatus(unittest.TestCase):
    """
    Test case for OccupancyStatus
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = OccupancyStatus.EMPTY

    @staticmethod
    def create_instance():
        """
        Create instance of OccupancyStatus
        """
        return OccupancyStatus.EMPTY

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(OccupancyStatus.EMPTY.value, 'EMPTY')
        self.assertEqual(OccupancyStatus.MANY_SEATS_AVAILABLE.value, 'MANY_SEATS_AVAILABLE')
        self.assertEqual(OccupancyStatus.FEW_SEATS_AVAILABLE.value, 'FEW_SEATS_AVAILABLE')
        self.assertEqual(OccupancyStatus.STANDING_ROOM_ONLY.value, 'STANDING_ROOM_ONLY')
        self.assertEqual(OccupancyStatus.CRUSHED_STANDING_ROOM_ONLY.value, 'CRUSHED_STANDING_ROOM_ONLY')
        self.assertEqual(OccupancyStatus.FULL.value, 'FULL')
        self.assertEqual(OccupancyStatus.NOT_ACCEPTING_PASSENGERS.value, 'NOT_ACCEPTING_PASSENGERS')