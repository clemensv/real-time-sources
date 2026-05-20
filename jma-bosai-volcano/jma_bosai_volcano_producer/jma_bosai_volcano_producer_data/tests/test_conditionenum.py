import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_producer_data.conditionenum import ConditionEnum


class Test_ConditionEnum(unittest.TestCase):
    """
    Test case for ConditionEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ConditionEnum.ISSUED

    @staticmethod
    def create_instance():
        """
        Create instance of ConditionEnum
        """
        return ConditionEnum.ISSUED

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ConditionEnum.ISSUED.value, "ISSUED")
        self.assertEqual(ConditionEnum.RAISED.value, "RAISED")
        self.assertEqual(ConditionEnum.LOWERED.value, "LOWERED")
        self.assertEqual(ConditionEnum.CONTINUED.value, "CONTINUED")
        self.assertEqual(ConditionEnum.SWITCHED.value, "SWITCHED")
        self.assertEqual(ConditionEnum.CANCELLED.value, "CANCELLED")