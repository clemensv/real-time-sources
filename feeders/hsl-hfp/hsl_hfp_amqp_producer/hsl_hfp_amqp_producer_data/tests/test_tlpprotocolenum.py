import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_amqp_producer_data.fi.hsl.hfp.tlpprotocolenum import TlpProtocolEnum


class Test_TlpProtocolEnum(unittest.TestCase):
    """
    Test case for TlpProtocolEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TlpProtocolEnum.MQTT

    @staticmethod
    def create_instance():
        """
        Create instance of TlpProtocolEnum
        """
        return TlpProtocolEnum.MQTT

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TlpProtocolEnum.MQTT.value, 'MQTT')
        self.assertEqual(TlpProtocolEnum.KAR_MINUSMQTT.value, 'KAR-MQTT')