import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_mqtt_producer_data.officeeventenum import OfficeEventEnum


class Test_OfficeEventEnum(unittest.TestCase):
    """
    Test case for OfficeEventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = OfficeEventEnum.info

    @staticmethod
    def create_instance():
        """
        Create instance of OfficeEventEnum
        """
        return OfficeEventEnum.info

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(OfficeEventEnum.info.value, 'info')