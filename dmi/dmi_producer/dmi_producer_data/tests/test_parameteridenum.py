import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.parameteridenum import ParameterIdenum


class Test_ParameterIdenum(unittest.TestCase):
    """
    Test case for ParameterIdenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ParameterIdenum.sealev_dvr

    @staticmethod
    def create_instance():
        """
        Create instance of ParameterIdenum
        """
        return ParameterIdenum.sealev_dvr

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ParameterIdenum.sealev_dvr.value, "sealev_dvr")
        self.assertEqual(ParameterIdenum.sealev_ln.value, "sealev_ln")
        self.assertEqual(ParameterIdenum.sea_reg.value, "sea_reg")
        self.assertEqual(ParameterIdenum.tw.value, "tw")