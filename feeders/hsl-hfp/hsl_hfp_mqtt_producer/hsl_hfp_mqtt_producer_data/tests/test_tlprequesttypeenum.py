import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.hfp.tlprequesttypeenum import TlpRequestTypeEnum


class Test_TlpRequestTypeEnum(unittest.TestCase):
    """
    Test case for TlpRequestTypeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TlpRequestTypeEnum.NORMAL

    @staticmethod
    def create_instance():
        """
        Create instance of TlpRequestTypeEnum
        """
        return TlpRequestTypeEnum.NORMAL

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TlpRequestTypeEnum.NORMAL.value, 'NORMAL')
        self.assertEqual(TlpRequestTypeEnum.DOOR_CLOSE.value, 'DOOR_CLOSE')
        self.assertEqual(TlpRequestTypeEnum.DOOR_OPEN.value, 'DOOR_OPEN')
        self.assertEqual(TlpRequestTypeEnum.ADVANCE.value, 'ADVANCE')