import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.congestionlevel import CongestionLevel


class Test_CongestionLevel(unittest.TestCase):
    """
    Test case for CongestionLevel
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = CongestionLevel.UNKNOWN_CONGESTION_LEVEL

    @staticmethod
    def create_instance():
        """
        Create instance of CongestionLevel
        """
        return CongestionLevel.UNKNOWN_CONGESTION_LEVEL

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(CongestionLevel.UNKNOWN_CONGESTION_LEVEL.value, 'UNKNOWN_CONGESTION_LEVEL')
        self.assertEqual(CongestionLevel.RUNNING_SMOOTHLY.value, 'RUNNING_SMOOTHLY')
        self.assertEqual(CongestionLevel.STOP_AND_GO.value, 'STOP_AND_GO')
        self.assertEqual(CongestionLevel.CONGESTION.value, 'CONGESTION')
        self.assertEqual(CongestionLevel.SEVERE_CONGESTION.value, 'SEVERE_CONGESTION')