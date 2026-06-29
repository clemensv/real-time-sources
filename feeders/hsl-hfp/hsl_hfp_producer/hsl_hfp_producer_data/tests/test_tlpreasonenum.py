import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_producer_data.fi.hsl.hfp.tlpreasonenum import TlpReasonEnum


class Test_TlpReasonEnum(unittest.TestCase):
    """
    Test case for TlpReasonEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TlpReasonEnum.GLOBAL

    @staticmethod
    def create_instance():
        """
        Create instance of TlpReasonEnum
        """
        return TlpReasonEnum.GLOBAL

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TlpReasonEnum.GLOBAL.value, 'GLOBAL')
        self.assertEqual(TlpReasonEnum.AHEAD.value, 'AHEAD')
        self.assertEqual(TlpReasonEnum.LINE.value, 'LINE')
        self.assertEqual(TlpReasonEnum.PRIOEXEP.value, 'PRIOEXEP')