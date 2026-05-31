import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_producer_data.jp.jma.amedas.eventenum import EventEnum


class Test_EventEnum(unittest.TestCase):
    """
    Test case for EventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = EventEnum.observation

    @staticmethod
    def create_instance():
        """
        Create instance of EventEnum
        """
        return EventEnum.observation

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(EventEnum.observation.value, 'observation')