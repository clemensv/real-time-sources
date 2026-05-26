import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_producer_data.jp.jma.amedas.stationtypeenum import StationTypeenum


class Test_StationTypeenum(unittest.TestCase):
    """
    Test case for StationTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = StationTypeenum.A

    @staticmethod
    def create_instance():
        """
        Create instance of StationTypeenum
        """
        return StationTypeenum.A

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(StationTypeenum.A.value, 'A')
        self.assertEqual(StationTypeenum.B.value, 'B')
        self.assertEqual(StationTypeenum.C.value, 'C')