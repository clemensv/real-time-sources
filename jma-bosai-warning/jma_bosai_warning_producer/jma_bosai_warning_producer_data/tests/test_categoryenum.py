import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.categoryenum import CategoryEnum


class Test_CategoryEnum(unittest.TestCase):
    """
    Test case for CategoryEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = CategoryEnum.MAJOR_WARNING

    @staticmethod
    def create_instance():
        """
        Create instance of CategoryEnum
        """
        return CategoryEnum.MAJOR_WARNING

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(CategoryEnum.MAJOR_WARNING.value, "MAJOR_WARNING")
        self.assertEqual(CategoryEnum.WARNING.value, "WARNING")
        self.assertEqual(CategoryEnum.ADVISORY.value, "ADVISORY")
        self.assertEqual(CategoryEnum.FORECAST.value, "FORECAST")