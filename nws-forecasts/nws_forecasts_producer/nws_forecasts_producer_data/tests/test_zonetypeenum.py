import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_forecasts_producer_data.zonetypeenum import ZoneTypeenum


class Test_ZoneTypeenum(unittest.TestCase):
    """
    Test case for ZoneTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ZoneTypeenum.public

    @staticmethod
    def create_instance():
        """
        Create instance of ZoneTypeenum
        """
        return ZoneTypeenum.public

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ZoneTypeenum.public.value, "public")
        self.assertEqual(ZoneTypeenum.coastal.value, "coastal")
        self.assertEqual(ZoneTypeenum.offshore.value, "offshore")
        self.assertEqual(ZoneTypeenum.marine.value, "marine")