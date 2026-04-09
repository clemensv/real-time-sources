import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_japan_producer_data.feedtypeenum import FeedTypeenum


class Test_FeedTypeenum(unittest.TestCase):
    """
    Test case for FeedTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = FeedTypeenum.regular

    @staticmethod
    def create_instance():
        """
        Create instance of FeedTypeenum
        """
        return FeedTypeenum.regular

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(FeedTypeenum.regular.value, "regular")
        self.assertEqual(FeedTypeenum.extra.value, "extra")