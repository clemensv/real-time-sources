import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.statusenum import StatusEnum


class Test_StatusEnum(unittest.TestCase):
    """
    Test case for StatusEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = StatusEnum.ISSUED

    @staticmethod
    def create_instance():
        """
        Create instance of StatusEnum
        """
        return StatusEnum.ISSUED

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(StatusEnum.ISSUED.value, 'ISSUED')
        self.assertEqual(StatusEnum.CONTINUED.value, 'CONTINUED')
        self.assertEqual(StatusEnum.CANCELLED.value, 'CANCELLED')
        self.assertEqual(StatusEnum.NO_WARNINGS_OR_ADVISORIES.value, 'NO_WARNINGS_OR_ADVISORIES')
        self.assertEqual(StatusEnum.WARNING.value, 'WARNING')
        self.assertEqual(StatusEnum.ADVISORY.value, 'ADVISORY')
        self.assertEqual(StatusEnum.EMERGENCY_WARNING.value, 'EMERGENCY_WARNING')