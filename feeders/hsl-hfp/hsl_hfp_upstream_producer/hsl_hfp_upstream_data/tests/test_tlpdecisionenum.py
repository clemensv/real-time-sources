import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_upstream_data.fi.hsl.hfp.tlpdecisionenum import TlpDecisionEnum


class Test_TlpDecisionEnum(unittest.TestCase):
    """
    Test case for TlpDecisionEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TlpDecisionEnum.ACK

    @staticmethod
    def create_instance():
        """
        Create instance of TlpDecisionEnum
        """
        return TlpDecisionEnum.ACK

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TlpDecisionEnum.ACK.value, 'ACK')
        self.assertEqual(TlpDecisionEnum.NAK.value, 'NAK')