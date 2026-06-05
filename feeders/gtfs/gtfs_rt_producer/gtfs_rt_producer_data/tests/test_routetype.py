import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.routetype import RouteType


class Test_RouteType(unittest.TestCase):
    """
    Test case for RouteType
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = RouteType.TRAM

    @staticmethod
    def create_instance():
        """
        Create instance of RouteType
        """
        return RouteType.TRAM

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(RouteType.TRAM.value, 'TRAM')
        self.assertEqual(RouteType.SUBWAY.value, 'SUBWAY')
        self.assertEqual(RouteType.RAIL.value, 'RAIL')
        self.assertEqual(RouteType.BUS.value, 'BUS')
        self.assertEqual(RouteType.FERRY.value, 'FERRY')
        self.assertEqual(RouteType.CABLE_TRAM.value, 'CABLE_TRAM')
        self.assertEqual(RouteType.AERIAL_LIFT.value, 'AERIAL_LIFT')
        self.assertEqual(RouteType.FUNICULAR.value, 'FUNICULAR')
        self.assertEqual(RouteType.RESERVED_1.value, 'RESERVED_1')
        self.assertEqual(RouteType.RESERVED_2.value, 'RESERVED_2')
        self.assertEqual(RouteType.RESERVED_3.value, 'RESERVED_3')
        self.assertEqual(RouteType.TROLLEYBUS.value, 'TROLLEYBUS')
        self.assertEqual(RouteType.MONORAIL.value, 'MONORAIL')
        self.assertEqual(RouteType.OTHER.value, 'OTHER')