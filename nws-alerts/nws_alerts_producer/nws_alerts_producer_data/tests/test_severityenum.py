import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_alerts_producer_data.severityenum import SeverityEnum


class Test_SeverityEnum(unittest.TestCase):
    """
    Test case for SeverityEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = SeverityEnum.Extreme

    @staticmethod
    def create_instance():
        """
        Create instance of SeverityEnum
        """
        return SeverityEnum.Extreme

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(SeverityEnum.Extreme.value, "Extreme")
        self.assertEqual(SeverityEnum.Severe.value, "Severe")
        self.assertEqual(SeverityEnum.Moderate.value, "Moderate")
        self.assertEqual(SeverityEnum.Minor.value, "Minor")
        self.assertEqual(SeverityEnum.Unknown.value, "Unknown")