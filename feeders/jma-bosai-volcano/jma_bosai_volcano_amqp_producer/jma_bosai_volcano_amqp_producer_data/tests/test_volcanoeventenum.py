import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_amqp_producer_data.volcanoeventenum import VolcanoEventEnum


class Test_VolcanoEventEnum(unittest.TestCase):
    """
    Test case for VolcanoEventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = VolcanoEventEnum.info

    @staticmethod
    def create_instance():
        """
        Create instance of VolcanoEventEnum
        """
        return VolcanoEventEnum.info

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(VolcanoEventEnum.info.value, 'info')