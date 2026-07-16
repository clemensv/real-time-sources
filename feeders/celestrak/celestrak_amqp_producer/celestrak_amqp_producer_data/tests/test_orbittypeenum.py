import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_amqp_producer_data.org.celestrak.orbittypeenum import OrbitTypeEnum


class Test_OrbitTypeEnum(unittest.TestCase):
    """
    Test case for OrbitTypeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = OrbitTypeEnum.ORB

    @staticmethod
    def create_instance():
        """
        Create instance of OrbitTypeEnum
        """
        return OrbitTypeEnum.ORB

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(OrbitTypeEnum.ORB.value, 'ORB')
        self.assertEqual(OrbitTypeEnum.LAN.value, 'LAN')
        self.assertEqual(OrbitTypeEnum.IMP.value, 'IMP')
        self.assertEqual(OrbitTypeEnum.DOC.value, 'DOC')
        self.assertEqual(OrbitTypeEnum.R_SLASHT.value, 'R/T')