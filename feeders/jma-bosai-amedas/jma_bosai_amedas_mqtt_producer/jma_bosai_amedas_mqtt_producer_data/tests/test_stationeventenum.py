import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.stationeventenum import StationEventEnum


class Test_StationEventEnum(unittest.TestCase):
    """
    Test case for StationEventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = StationEventEnum.info

    @staticmethod
    def create_instance():
        """
        Create instance of StationEventEnum
        """
        return StationEventEnum.info

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(StationEventEnum.info.value, 'info')