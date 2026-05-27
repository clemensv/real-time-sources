import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_mqtt_producer_data.uk.kcl.laqn.sitetypeenum import SiteTypeenum


class Test_SiteTypeenum(unittest.TestCase):
    """
    Test case for SiteTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = SiteTypeenum.Suburban

    @staticmethod
    def create_instance():
        """
        Create instance of SiteTypeenum
        """
        return SiteTypeenum.Suburban

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(SiteTypeenum.Suburban.value, 'Suburban')
        self.assertEqual(SiteTypeenum.Kerbside.value, 'Kerbside')
        self.assertEqual(SiteTypeenum.Roadside.value, 'Roadside')
        self.assertEqual(SiteTypeenum.Urban_Background.value, 'Urban Background')
        self.assertEqual(SiteTypeenum.Industrial.value, 'Industrial')
        self.assertEqual(SiteTypeenum.Rural.value, 'Rural')
        self.assertEqual(SiteTypeenum.other.value, 'other')