import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_producer_data.volcanicwarningeventenum import VolcanicWarningEventEnum


class Test_VolcanicWarningEventEnum(unittest.TestCase):
    """
    Test case for VolcanicWarningEventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = VolcanicWarningEventEnum.warning

    @staticmethod
    def create_instance():
        """
        Create instance of VolcanicWarningEventEnum
        """
        return VolcanicWarningEventEnum.warning

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(VolcanicWarningEventEnum.warning.value, 'warning')