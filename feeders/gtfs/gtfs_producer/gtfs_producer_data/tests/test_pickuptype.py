import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.pickuptype import PickupType


class Test_PickupType(unittest.TestCase):
    """
    Test case for PickupType
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = PickupType.REGULAR

    @staticmethod
    def create_instance():
        """
        Create instance of PickupType
        """
        return PickupType.REGULAR

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(PickupType.REGULAR.value, 'REGULAR')
        self.assertEqual(PickupType.NO_PICKUP.value, 'NO_PICKUP')
        self.assertEqual(PickupType.PHONE_AGENCY.value, 'PHONE_AGENCY')
        self.assertEqual(PickupType.COORDINATE_WITH_DRIVER.value, 'COORDINATE_WITH_DRIVER')