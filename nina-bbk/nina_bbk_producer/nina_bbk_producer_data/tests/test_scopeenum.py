import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nina_bbk_producer_data.scopeenum import ScopeEnum


class Test_ScopeEnum(unittest.TestCase):
    """
    Test case for ScopeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ScopeEnum.Public

    @staticmethod
    def create_instance():
        """
        Create instance of ScopeEnum
        """
        return ScopeEnum.Public

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ScopeEnum.Public.value, "Public")
        self.assertEqual(ScopeEnum.Restricted.value, "Restricted")
        self.assertEqual(ScopeEnum.Private.value, "Private")