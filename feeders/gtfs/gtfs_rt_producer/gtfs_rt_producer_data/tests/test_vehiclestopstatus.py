import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.vehiclestopstatus import VehicleStopStatus


class Test_VehicleStopStatus(unittest.TestCase):
    """
    Test case for VehicleStopStatus
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = VehicleStopStatus.INCOMING_AT

    @staticmethod
    def create_instance():
        """
        Create instance of VehicleStopStatus
        """
        return VehicleStopStatus.INCOMING_AT

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(VehicleStopStatus.INCOMING_AT.value, 'INCOMING_AT')
        self.assertEqual(VehicleStopStatus.STOPPED_AT.value, 'STOPPED_AT')
        self.assertEqual(VehicleStopStatus.IN_TRANSIT_TO.value, 'IN_TRANSIT_TO')