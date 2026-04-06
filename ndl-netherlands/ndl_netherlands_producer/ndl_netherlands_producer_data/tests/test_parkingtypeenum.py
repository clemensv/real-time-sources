import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.parkingtypeenum import ParkingTypeenum


class Test_ParkingTypeenum(unittest.TestCase):
    """
    Test case for ParkingTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ParkingTypeenum.ALONG_MOTORWAY

    @staticmethod
    def create_instance():
        """
        Create instance of ParkingTypeenum
        """
        return ParkingTypeenum.ALONG_MOTORWAY

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ParkingTypeenum.ALONG_MOTORWAY.value, "ALONG_MOTORWAY")
        self.assertEqual(ParkingTypeenum.PARKING_GARAGE.value, "PARKING_GARAGE")
        self.assertEqual(ParkingTypeenum.PARKING_LOT.value, "PARKING_LOT")
        self.assertEqual(ParkingTypeenum.ON_DRIVEWAY.value, "ON_DRIVEWAY")
        self.assertEqual(ParkingTypeenum.ON_STREET.value, "ON_STREET")
        self.assertEqual(ParkingTypeenum.UNDERGROUND_GARAGE.value, "UNDERGROUND_GARAGE")
        self.assertEqual(ParkingTypeenum.None.value, "None")