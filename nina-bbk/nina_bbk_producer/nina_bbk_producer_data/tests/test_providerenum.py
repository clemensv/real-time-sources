import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nina_bbk_producer_data.providerenum import ProviderEnum


class Test_ProviderEnum(unittest.TestCase):
    """
    Test case for ProviderEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ProviderEnum.mowas

    @staticmethod
    def create_instance():
        """
        Create instance of ProviderEnum
        """
        return ProviderEnum.mowas

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ProviderEnum.mowas.value, "mowas")
        self.assertEqual(ProviderEnum.katwarn.value, "katwarn")
        self.assertEqual(ProviderEnum.biwapp.value, "biwapp")
        self.assertEqual(ProviderEnum.dwd.value, "dwd")
        self.assertEqual(ProviderEnum.lhp.value, "lhp")
        self.assertEqual(ProviderEnum.police.value, "police")