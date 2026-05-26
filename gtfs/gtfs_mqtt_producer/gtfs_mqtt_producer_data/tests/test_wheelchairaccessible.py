import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.wheelchairaccessible import WheelchairAccessible


class Test_WheelchairAccessible(unittest.TestCase):
    """
    Test case for WheelchairAccessible
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = WheelchairAccessible.NO_INFO

    @staticmethod
    def create_instance():
        """
        Create instance of WheelchairAccessible
        """
        return WheelchairAccessible.NO_INFO

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(WheelchairAccessible.NO_INFO.value, 'NO_INFO')
        self.assertEqual(WheelchairAccessible.WHEELCHAIR_ACCESSIBLE.value, 'WHEELCHAIR_ACCESSIBLE')
        self.assertEqual(WheelchairAccessible.NOT_WHEELCHAIR_ACCESSIBLE.value, 'NOT_WHEELCHAIR_ACCESSIBLE')