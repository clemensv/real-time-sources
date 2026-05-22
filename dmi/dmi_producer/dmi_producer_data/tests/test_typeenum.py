import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.typeenum import TypeEnum


class Test_TypeEnum(unittest.TestCase):
    """
    Test case for TypeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TypeEnum.0

    @staticmethod
    def create_instance():
        """
        Create instance of TypeEnum
        """
        return TypeEnum.0

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TypeEnum.0.value, "0")
        self.assertEqual(TypeEnum.1.value, "1")
        self.assertEqual(TypeEnum.2.value, "2")