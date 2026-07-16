import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_mqtt_producer_data.org.celestrak.classificationtypeenum import ClassificationTypeEnum


class Test_ClassificationTypeEnum(unittest.TestCase):
    """
    Test case for ClassificationTypeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ClassificationTypeEnum.U

    @staticmethod
    def create_instance():
        """
        Create instance of ClassificationTypeEnum
        """
        return ClassificationTypeEnum.U

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ClassificationTypeEnum.U.value, 'U')
        self.assertEqual(ClassificationTypeEnum.C.value, 'C')
        self.assertEqual(ClassificationTypeEnum.S.value, 'S')