import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_amqp_producer_data.fi.hsl.hfp.tlpprioritylevelenum import TlpPriorityLevelEnum


class Test_TlpPriorityLevelEnum(unittest.TestCase):
    """
    Test case for TlpPriorityLevelEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TlpPriorityLevelEnum.normal

    @staticmethod
    def create_instance():
        """
        Create instance of TlpPriorityLevelEnum
        """
        return TlpPriorityLevelEnum.normal

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TlpPriorityLevelEnum.normal.value, 'normal')
        self.assertEqual(TlpPriorityLevelEnum.high.value, 'high')
        self.assertEqual(TlpPriorityLevelEnum.norequest.value, 'norequest')