import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ptwc_tsunami_producer_data.categoryenum import CategoryEnum


class Test_CategoryEnum(unittest.TestCase):
    """
    Test case for CategoryEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = CategoryEnum.Warning

    @staticmethod
    def create_instance():
        """
        Create instance of CategoryEnum
        """
        return CategoryEnum.Warning

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(CategoryEnum.Warning.value, "Warning")
        self.assertEqual(CategoryEnum.Advisory.value, "Advisory")
        self.assertEqual(CategoryEnum.Watch.value, "Watch")
        self.assertEqual(CategoryEnum.Information.value, "Information")