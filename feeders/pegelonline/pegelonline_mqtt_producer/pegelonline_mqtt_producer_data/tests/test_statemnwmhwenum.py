import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_mqtt_producer_data.de.wsv.pegelonline.statemnwmhwenum import StateMnwMhwEnum


class Test_StateMnwMhwEnum(unittest.TestCase):
    """
    Test case for StateMnwMhwEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = StateMnwMhwEnum.low

    @staticmethod
    def create_instance():
        """
        Create instance of StateMnwMhwEnum
        """
        return StateMnwMhwEnum.low

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(StateMnwMhwEnum.low.value, 'low')
        self.assertEqual(StateMnwMhwEnum.normal.value, 'normal')
        self.assertEqual(StateMnwMhwEnum.high.value, 'high')
        self.assertEqual(StateMnwMhwEnum.unknown.value, 'unknown')
        self.assertEqual(StateMnwMhwEnum.commented.value, 'commented')
        self.assertEqual(StateMnwMhwEnum.out_MINUSdated.value, 'out-dated')