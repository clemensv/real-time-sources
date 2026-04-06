import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.reservationenum import ReservationEnum


class Test_ReservationEnum(unittest.TestCase):
    """
    Test case for ReservationEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ReservationEnum.RESERVATION

    @staticmethod
    def create_instance():
        """
        Create instance of ReservationEnum
        """
        return ReservationEnum.RESERVATION

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ReservationEnum.RESERVATION.value, "RESERVATION")
        self.assertEqual(ReservationEnum.RESERVATION_EXPIRES.value, "RESERVATION_EXPIRES")
        self.assertEqual(ReservationEnum.None.value, "None")