import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_producer_data.de.wsv.pegelonline.statenswhswenum import StateNswHswEnum


class Test_StateNswHswEnum(unittest.TestCase):
    """
    Test case for StateNswHswEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = StateNswHswEnum.normal

    @staticmethod
    def create_instance():
        """
        Create instance of StateNswHswEnum
        """
        return StateNswHswEnum.normal

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(StateNswHswEnum.normal.value, 'normal')
        self.assertEqual(StateNswHswEnum.high.value, 'high')
        self.assertEqual(StateNswHswEnum.unknown.value, 'unknown')
        self.assertEqual(StateNswHswEnum.commented.value, 'commented')
        self.assertEqual(StateNswHswEnum.out_MINUSdated.value, 'out-dated')