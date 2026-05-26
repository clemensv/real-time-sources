import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_amqp_producer_data.eventenum import EventEnum


class Test_EventEnum(unittest.TestCase):
    """
    Test case for EventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = EventEnum.info

    @staticmethod
    def create_instance():
        """
        Create instance of EventEnum
        """
        return EventEnum.info

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(EventEnum.info.value, 'info')