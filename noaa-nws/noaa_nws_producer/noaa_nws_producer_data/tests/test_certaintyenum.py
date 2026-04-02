import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_producer_data.certaintyenum import CertaintyEnum


class Test_CertaintyEnum(unittest.TestCase):
    """
    Test case for CertaintyEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = CertaintyEnum.Observed

    @staticmethod
    def create_instance():
        """
        Create instance of CertaintyEnum
        """
        return CertaintyEnum.Observed

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(CertaintyEnum.Observed.value, "Observed")
        self.assertEqual(CertaintyEnum.Likely.value, "Likely")
        self.assertEqual(CertaintyEnum.Possible.value, "Possible")
        self.assertEqual(CertaintyEnum.Unlikely.value, "Unlikely")
        self.assertEqual(CertaintyEnum.Unknown.value, "Unknown")