import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.statusenum import StatusEnum


class Test_StatusEnum(unittest.TestCase):
    """
    Test case for StatusEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = StatusEnum.AVAILABLE

    @staticmethod
    def create_instance():
        """
        Create instance of StatusEnum
        """
        return StatusEnum.AVAILABLE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(StatusEnum.AVAILABLE.value, "AVAILABLE")
        self.assertEqual(StatusEnum.BLOCKED.value, "BLOCKED")
        self.assertEqual(StatusEnum.CHARGING.value, "CHARGING")
        self.assertEqual(StatusEnum.INOPERATIVE.value, "INOPERATIVE")
        self.assertEqual(StatusEnum.OUTOFORDER.value, "OUTOFORDER")
        self.assertEqual(StatusEnum.PLANNED.value, "PLANNED")
        self.assertEqual(StatusEnum.REMOVED.value, "REMOVED")
        self.assertEqual(StatusEnum.RESERVED.value, "RESERVED")
        self.assertEqual(StatusEnum.UNKNOWN.value, "UNKNOWN")