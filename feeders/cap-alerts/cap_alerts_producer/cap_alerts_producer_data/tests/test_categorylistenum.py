import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_producer_data.org.oasis.cap.alerts.categorylistenum import CategoryListEnum


class Test_CategoryListEnum(unittest.TestCase):
    """
    Test case for CategoryListEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = CategoryListEnum.Geo

    @staticmethod
    def create_instance():
        """
        Create instance of CategoryListEnum
        """
        return CategoryListEnum.Geo

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(CategoryListEnum.Geo.value, 'Geo')
        self.assertEqual(CategoryListEnum.Met.value, 'Met')
        self.assertEqual(CategoryListEnum.Safety.value, 'Safety')
        self.assertEqual(CategoryListEnum.Security.value, 'Security')
        self.assertEqual(CategoryListEnum.Rescue.value, 'Rescue')
        self.assertEqual(CategoryListEnum.Fire.value, 'Fire')
        self.assertEqual(CategoryListEnum.Health.value, 'Health')
        self.assertEqual(CategoryListEnum.Env.value, 'Env')
        self.assertEqual(CategoryListEnum.Transport.value, 'Transport')
        self.assertEqual(CategoryListEnum.Infra.value, 'Infra')
        self.assertEqual(CategoryListEnum.CBRNE.value, 'CBRNE')
        self.assertEqual(CategoryListEnum.Other.value, 'Other')