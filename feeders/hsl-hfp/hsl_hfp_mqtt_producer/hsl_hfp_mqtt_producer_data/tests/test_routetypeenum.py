import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.gtfs.routetypeenum import RouteTypeenum


class Test_RouteTypeenum(unittest.TestCase):
    """
    Test case for RouteTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = RouteTypeenum.VALUE_0

    @staticmethod
    def create_instance():
        """
        Create instance of RouteTypeenum
        """
        return RouteTypeenum.VALUE_0

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(RouteTypeenum.VALUE_0.value, 0)
        self.assertEqual(RouteTypeenum.VALUE_1.value, 1)
        self.assertEqual(RouteTypeenum.VALUE_2.value, 2)
        self.assertEqual(RouteTypeenum.VALUE_3.value, 3)
        self.assertEqual(RouteTypeenum.VALUE_4.value, 4)
        self.assertEqual(RouteTypeenum.VALUE_5.value, 5)
        self.assertEqual(RouteTypeenum.VALUE_6.value, 6)
        self.assertEqual(RouteTypeenum.VALUE_7.value, 7)
        self.assertEqual(RouteTypeenum.VALUE_11.value, 11)
        self.assertEqual(RouteTypeenum.VALUE_12.value, 12)