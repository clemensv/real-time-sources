import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.bikesallowed import BikesAllowed


class Test_BikesAllowed(unittest.TestCase):
    """
    Test case for BikesAllowed
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = BikesAllowed.NO_INFO

    @staticmethod
    def create_instance():
        """
        Create instance of BikesAllowed
        """
        return BikesAllowed.NO_INFO

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(BikesAllowed.NO_INFO.value, 'NO_INFO')
        self.assertEqual(BikesAllowed.BICYCLE_ALLOWED.value, 'BICYCLE_ALLOWED')
        self.assertEqual(BikesAllowed.BICYCLE_NOT_ALLOWED.value, 'BICYCLE_NOT_ALLOWED')