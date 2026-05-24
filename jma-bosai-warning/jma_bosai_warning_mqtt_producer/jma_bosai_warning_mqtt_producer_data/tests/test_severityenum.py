import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_mqtt_producer_data.severityenum import SeverityEnum


class Test_SeverityEnum(unittest.TestCase):
    """
    Test case for SeverityEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = SeverityEnum.REFERENCE

    @staticmethod
    def create_instance():
        """
        Create instance of SeverityEnum
        """
        return SeverityEnum.REFERENCE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(SeverityEnum.REFERENCE.value, 'REFERENCE')
        self.assertEqual(SeverityEnum.NONE.value, 'NONE')
        self.assertEqual(SeverityEnum.ADVISORY.value, 'ADVISORY')
        self.assertEqual(SeverityEnum.WARNING.value, 'WARNING')
        self.assertEqual(SeverityEnum.EMERGENCY_WARNING.value, 'EMERGENCY_WARNING')