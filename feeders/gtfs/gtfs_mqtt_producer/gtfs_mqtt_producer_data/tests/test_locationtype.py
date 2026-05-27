import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.locationtype import LocationType


class Test_LocationType(unittest.TestCase):
    """
    Test case for LocationType
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = LocationType.STOP

    @staticmethod
    def create_instance():
        """
        Create instance of LocationType
        """
        return LocationType.STOP

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(LocationType.STOP.value, 'STOP')
        self.assertEqual(LocationType.STATION.value, 'STATION')
        self.assertEqual(LocationType.ENTRANCE_EXIT.value, 'ENTRANCE_EXIT')
        self.assertEqual(LocationType.GENERIC_NODE.value, 'GENERIC_NODE')
        self.assertEqual(LocationType.BOARDING_AREA.value, 'BOARDING_AREA')