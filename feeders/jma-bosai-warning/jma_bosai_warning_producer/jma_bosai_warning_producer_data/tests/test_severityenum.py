import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.severityenum import SeverityEnum


class Test_SeverityEnum(unittest.TestCase):
    """
    Test case for SeverityEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = SeverityEnum.advisory

    @staticmethod
    def create_instance():
        """
        Create instance of SeverityEnum
        """
        return SeverityEnum.advisory

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(SeverityEnum.advisory.value, 'advisory')
        self.assertEqual(SeverityEnum.warning.value, 'warning')
        self.assertEqual(SeverityEnum.emergency.value, 'emergency')