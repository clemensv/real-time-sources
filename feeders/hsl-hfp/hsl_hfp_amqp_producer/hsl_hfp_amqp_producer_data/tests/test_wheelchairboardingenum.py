import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_amqp_producer_data.fi.hsl.gtfs.wheelchairboardingenum import WheelchairBoardingenum


class Test_WheelchairBoardingenum(unittest.TestCase):
    """
    Test case for WheelchairBoardingenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = WheelchairBoardingenum.VALUE_0

    @staticmethod
    def create_instance():
        """
        Create instance of WheelchairBoardingenum
        """
        return WheelchairBoardingenum.VALUE_0

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(WheelchairBoardingenum.VALUE_0.value, 0)
        self.assertEqual(WheelchairBoardingenum.VALUE_1.value, 1)
        self.assertEqual(WheelchairBoardingenum.VALUE_2.value, 2)