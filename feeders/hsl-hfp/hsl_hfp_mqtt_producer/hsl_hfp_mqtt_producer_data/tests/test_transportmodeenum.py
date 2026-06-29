import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.hfp.transportmodeenum import TransportModeEnum


class Test_TransportModeEnum(unittest.TestCase):
    """
    Test case for TransportModeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TransportModeEnum.bus

    @staticmethod
    def create_instance():
        """
        Create instance of TransportModeEnum
        """
        return TransportModeEnum.bus

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TransportModeEnum.bus.value, 'bus')
        self.assertEqual(TransportModeEnum.tram.value, 'tram')
        self.assertEqual(TransportModeEnum.train.value, 'train')
        self.assertEqual(TransportModeEnum.ferry.value, 'ferry')
        self.assertEqual(TransportModeEnum.metro.value, 'metro')
        self.assertEqual(TransportModeEnum.ubus.value, 'ubus')
        self.assertEqual(TransportModeEnum.robot.value, 'robot')