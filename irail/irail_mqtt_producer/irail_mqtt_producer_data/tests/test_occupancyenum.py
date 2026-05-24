import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_mqtt_producer_data.be.irail.occupancyenum import OccupancyEnum


class Test_OccupancyEnum(unittest.TestCase):
    """
    Test case for OccupancyEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = OccupancyEnum.low

    @staticmethod
    def create_instance():
        """
        Create instance of OccupancyEnum
        """
        return OccupancyEnum.low

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(OccupancyEnum.low.value, 'low')
        self.assertEqual(OccupancyEnum.medium.value, 'medium')
        self.assertEqual(OccupancyEnum.high.value, 'high')
        self.assertEqual(OccupancyEnum.unknown.value, 'unknown')