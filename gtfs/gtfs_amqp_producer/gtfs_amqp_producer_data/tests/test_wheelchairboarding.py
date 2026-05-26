import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.wheelchairboarding import WheelchairBoarding


class Test_WheelchairBoarding(unittest.TestCase):
    """
    Test case for WheelchairBoarding
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = WheelchairBoarding.NO_INFO

    @staticmethod
    def create_instance():
        """
        Create instance of WheelchairBoarding
        """
        return WheelchairBoarding.NO_INFO

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(WheelchairBoarding.NO_INFO.value, 'NO_INFO')
        self.assertEqual(WheelchairBoarding.SOME_VEHICLES.value, 'SOME_VEHICLES')
        self.assertEqual(WheelchairBoarding.NOT_POSSIBLE.value, 'NOT_POSSIBLE')