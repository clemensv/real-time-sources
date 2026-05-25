import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.continuouspickup import ContinuousPickup


class Test_ContinuousPickup(unittest.TestCase):
    """
    Test case for ContinuousPickup
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ContinuousPickup.CONTINUOUS_STOPPING

    @staticmethod
    def create_instance():
        """
        Create instance of ContinuousPickup
        """
        return ContinuousPickup.CONTINUOUS_STOPPING

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ContinuousPickup.CONTINUOUS_STOPPING.value, 'CONTINUOUS_STOPPING')
        self.assertEqual(ContinuousPickup.NO_CONTINUOUS_STOPPING.value, 'NO_CONTINUOUS_STOPPING')
        self.assertEqual(ContinuousPickup.PHONE_AGENCY.value, 'PHONE_AGENCY')
        self.assertEqual(ContinuousPickup.COORDINATE_WITH_DRIVER.value, 'COORDINATE_WITH_DRIVER')