import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ptwc_tsunami_amqp_producer_data.basinenum import BasinEnum


class Test_BasinEnum(unittest.TestCase):
    """
    Test case for BasinEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = BasinEnum.pacific

    @staticmethod
    def create_instance():
        """
        Create instance of BasinEnum
        """
        return BasinEnum.pacific

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(BasinEnum.pacific.value, 'pacific')
        self.assertEqual(BasinEnum.alaska.value, 'alaska')
        self.assertEqual(BasinEnum.unknown.value, 'unknown')