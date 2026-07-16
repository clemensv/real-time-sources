import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_producer_data.org.celestrak.objecttypeenum import ObjectTypeEnum


class Test_ObjectTypeEnum(unittest.TestCase):
    """
    Test case for ObjectTypeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ObjectTypeEnum.PAY

    @staticmethod
    def create_instance():
        """
        Create instance of ObjectTypeEnum
        """
        return ObjectTypeEnum.PAY

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ObjectTypeEnum.PAY.value, 'PAY')
        self.assertEqual(ObjectTypeEnum.R_SLASHB.value, 'R/B')
        self.assertEqual(ObjectTypeEnum.DEB.value, 'DEB')
        self.assertEqual(ObjectTypeEnum.UNK.value, 'UNK')