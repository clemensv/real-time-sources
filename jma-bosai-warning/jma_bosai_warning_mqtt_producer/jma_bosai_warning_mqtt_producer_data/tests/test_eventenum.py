import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_mqtt_producer_data.eventenum import EventEnum


class Test_EventEnum(unittest.TestCase):
    """
    Test case for EventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = EventEnum.office

    @staticmethod
    def create_instance():
        """
        Create instance of EventEnum
        """
        return EventEnum.office

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(EventEnum.office.value, 'office')