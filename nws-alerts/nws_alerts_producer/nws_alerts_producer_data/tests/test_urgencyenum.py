import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_alerts_producer_data.urgencyenum import UrgencyEnum


class Test_UrgencyEnum(unittest.TestCase):
    """
    Test case for UrgencyEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = UrgencyEnum.Immediate

    @staticmethod
    def create_instance():
        """
        Create instance of UrgencyEnum
        """
        return UrgencyEnum.Immediate

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(UrgencyEnum.Immediate.value, "Immediate")
        self.assertEqual(UrgencyEnum.Expected.value, "Expected")
        self.assertEqual(UrgencyEnum.Future.value, "Future")
        self.assertEqual(UrgencyEnum.Past.value, "Past")
        self.assertEqual(UrgencyEnum.Unknown.value, "Unknown")