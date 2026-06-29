import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_amqp_producer_data.fi.hsl.gtfs.locationtypeenum import LocationTypeenum


class Test_LocationTypeenum(unittest.TestCase):
    """
    Test case for LocationTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = LocationTypeenum.VALUE_0

    @staticmethod
    def create_instance():
        """
        Create instance of LocationTypeenum
        """
        return LocationTypeenum.VALUE_0

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(LocationTypeenum.VALUE_0.value, 0)
        self.assertEqual(LocationTypeenum.VALUE_1.value, 1)
        self.assertEqual(LocationTypeenum.VALUE_2.value, 2)
        self.assertEqual(LocationTypeenum.VALUE_3.value, 3)
        self.assertEqual(LocationTypeenum.VALUE_4.value, 4)