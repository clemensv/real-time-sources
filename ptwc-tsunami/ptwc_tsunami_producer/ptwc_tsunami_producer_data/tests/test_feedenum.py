import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ptwc_tsunami_producer_data.feedenum import FeedEnum


class Test_FeedEnum(unittest.TestCase):
    """
    Test case for FeedEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = FeedEnum.PAAQ

    @staticmethod
    def create_instance():
        """
        Create instance of FeedEnum
        """
        return FeedEnum.PAAQ

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(FeedEnum.PAAQ.value, "PAAQ")
        self.assertEqual(FeedEnum.PHEB.value, "PHEB")