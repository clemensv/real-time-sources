import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_mqtt_producer_data.volcaniceruptioneventenum import VolcanicEruptionEventEnum


class Test_VolcanicEruptionEventEnum(unittest.TestCase):
    """
    Test case for VolcanicEruptionEventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = VolcanicEruptionEventEnum.eruption

    @staticmethod
    def create_instance():
        """
        Create instance of VolcanicEruptionEventEnum
        """
        return VolcanicEruptionEventEnum.eruption

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(VolcanicEruptionEventEnum.eruption.value, 'eruption')