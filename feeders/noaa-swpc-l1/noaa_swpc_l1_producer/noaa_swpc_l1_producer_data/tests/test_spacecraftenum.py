import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_swpc_l1_producer_data.gov.noaa.swpc.l1.spacecraftenum import SpacecraftEnum


class Test_SpacecraftEnum(unittest.TestCase):
    """
    Test case for SpacecraftEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = SpacecraftEnum.dscovr

    @staticmethod
    def create_instance():
        """
        Create instance of SpacecraftEnum
        """
        return SpacecraftEnum.dscovr

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(SpacecraftEnum.dscovr.value, 'dscovr')
        self.assertEqual(SpacecraftEnum.ace.value, 'ace')