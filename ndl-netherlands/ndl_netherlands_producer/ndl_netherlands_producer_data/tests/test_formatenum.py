import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.formatenum import FormatEnum


class Test_FormatEnum(unittest.TestCase):
    """
    Test case for FormatEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = FormatEnum.SOCKET

    @staticmethod
    def create_instance():
        """
        Create instance of FormatEnum
        """
        return FormatEnum.SOCKET

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(FormatEnum.SOCKET.value, "SOCKET")
        self.assertEqual(FormatEnum.CABLE.value, "CABLE")