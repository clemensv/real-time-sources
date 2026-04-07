import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from meteoalarm_producer_data.statusenum import StatusEnum


class Test_StatusEnum(unittest.TestCase):
    """
    Test case for StatusEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = StatusEnum.Actual

    @staticmethod
    def create_instance():
        """
        Create instance of StatusEnum
        """
        return StatusEnum.Actual

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(StatusEnum.Actual.value, "Actual")
        self.assertEqual(StatusEnum.Exercise.value, "Exercise")
        self.assertEqual(StatusEnum.System.value, "System")
        self.assertEqual(StatusEnum.Test.value, "Test")
        self.assertEqual(StatusEnum.Draft.value, "Draft")