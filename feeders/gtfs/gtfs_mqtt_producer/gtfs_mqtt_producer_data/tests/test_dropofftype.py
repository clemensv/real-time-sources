import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.dropofftype import DropOffType


class Test_DropOffType(unittest.TestCase):
    """
    Test case for DropOffType
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = DropOffType.REGULAR

    @staticmethod
    def create_instance():
        """
        Create instance of DropOffType
        """
        return DropOffType.REGULAR

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(DropOffType.REGULAR.value, 'REGULAR')
        self.assertEqual(DropOffType.NO_DROP_OFF.value, 'NO_DROP_OFF')
        self.assertEqual(DropOffType.PHONE_AGENCY.value, 'PHONE_AGENCY')
        self.assertEqual(DropOffType.COORDINATE_WITH_DRIVER.value, 'COORDINATE_WITH_DRIVER')