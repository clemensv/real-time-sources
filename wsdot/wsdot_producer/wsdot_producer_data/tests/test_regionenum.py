import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.traffic.regionenum import RegionEnum


class Test_RegionEnum(unittest.TestCase):
    """
    Test case for RegionEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = RegionEnum.Eastern

    @staticmethod
    def create_instance():
        """
        Create instance of RegionEnum
        """
        return RegionEnum.Eastern

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(RegionEnum.Eastern.value, 'Eastern')
        self.assertEqual(RegionEnum.Northwest.value, 'Northwest')
        self.assertEqual(RegionEnum.Olympic.value, 'Olympic')
        self.assertEqual(RegionEnum.Southwest.value, 'Southwest')