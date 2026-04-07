import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nina_bbk_producer_data.categoryenum import CategoryEnum


class Test_CategoryEnum(unittest.TestCase):
    """
    Test case for CategoryEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = CategoryEnum.Met

    @staticmethod
    def create_instance():
        """
        Create instance of CategoryEnum
        """
        return CategoryEnum.Met

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(CategoryEnum.Met.value, "Met")
        self.assertEqual(CategoryEnum.Geo.value, "Geo")
        self.assertEqual(CategoryEnum.Safety.value, "Safety")
        self.assertEqual(CategoryEnum.Security.value, "Security")
        self.assertEqual(CategoryEnum.Rescue.value, "Rescue")
        self.assertEqual(CategoryEnum.Fire.value, "Fire")
        self.assertEqual(CategoryEnum.Health.value, "Health")
        self.assertEqual(CategoryEnum.Env.value, "Env")
        self.assertEqual(CategoryEnum.Transport.value, "Transport")
        self.assertEqual(CategoryEnum.Infra.value, "Infra")
        self.assertEqual(CategoryEnum.CBRNE.value, "CBRNE")
        self.assertEqual(CategoryEnum.Other.value, "Other")