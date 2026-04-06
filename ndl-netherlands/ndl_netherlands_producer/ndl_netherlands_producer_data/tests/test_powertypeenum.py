import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.powertypeenum import PowerTypeenum


class Test_PowerTypeenum(unittest.TestCase):
    """
    Test case for PowerTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = PowerTypeenum.AC_1_PHASE

    @staticmethod
    def create_instance():
        """
        Create instance of PowerTypeenum
        """
        return PowerTypeenum.AC_1_PHASE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(PowerTypeenum.AC_1_PHASE.value, "AC_1_PHASE")
        self.assertEqual(PowerTypeenum.AC_2_PHASE.value, "AC_2_PHASE")
        self.assertEqual(PowerTypeenum.AC_2_PHASE_SPLIT.value, "AC_2_PHASE_SPLIT")
        self.assertEqual(PowerTypeenum.AC_3_PHASE.value, "AC_3_PHASE")
        self.assertEqual(PowerTypeenum.DC.value, "DC")