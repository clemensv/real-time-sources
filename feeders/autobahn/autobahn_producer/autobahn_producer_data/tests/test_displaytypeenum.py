import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_producer_data.displaytypeenum import DisplayTypeenum


class Test_DisplayTypeenum(unittest.TestCase):
    """
    Test case for DisplayTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = DisplayTypeenum.ELECTRIC_CHARGING_STATION

    @staticmethod
    def create_instance():
        """
        Create instance of DisplayTypeenum
        """
        return DisplayTypeenum.ELECTRIC_CHARGING_STATION

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(DisplayTypeenum.ELECTRIC_CHARGING_STATION.value, 'ELECTRIC_CHARGING_STATION')
        self.assertEqual(DisplayTypeenum.STRONG_ELECTRIC_CHARGING_STATION.value, 'STRONG_ELECTRIC_CHARGING_STATION')