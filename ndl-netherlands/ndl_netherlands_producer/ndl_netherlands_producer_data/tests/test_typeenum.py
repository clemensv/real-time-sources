import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.typeenum import TypeEnum


class Test_TypeEnum(unittest.TestCase):
    """
    Test case for TypeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TypeEnum.ENERGY

    @staticmethod
    def create_instance():
        """
        Create instance of TypeEnum
        """
        return TypeEnum.ENERGY

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TypeEnum.ENERGY.value, "ENERGY")
        self.assertEqual(TypeEnum.FLAT.value, "FLAT")
        self.assertEqual(TypeEnum.PARKING_TIME.value, "PARKING_TIME")
        self.assertEqual(TypeEnum.TIME.value, "TIME")