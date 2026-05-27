import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_mqtt_producer_data.alertlevelcodeenum import AlertLevelCodeenum


class Test_AlertLevelCodeenum(unittest.TestCase):
    """
    Test case for AlertLevelCodeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = AlertLevelCodeenum.CODE_02

    @staticmethod
    def create_instance():
        """
        Create instance of AlertLevelCodeenum
        """
        return AlertLevelCodeenum.CODE_02

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(AlertLevelCodeenum.CODE_02.value, 'CODE_02')
        self.assertEqual(AlertLevelCodeenum.CODE_03.value, 'CODE_03')
        self.assertEqual(AlertLevelCodeenum.CODE_04.value, 'CODE_04')
        self.assertEqual(AlertLevelCodeenum.CODE_11.value, 'CODE_11')
        self.assertEqual(AlertLevelCodeenum.CODE_12.value, 'CODE_12')
        self.assertEqual(AlertLevelCodeenum.CODE_13.value, 'CODE_13')
        self.assertEqual(AlertLevelCodeenum.CODE_22.value, 'CODE_22')
        self.assertEqual(AlertLevelCodeenum.CODE_23.value, 'CODE_23')
        self.assertEqual(AlertLevelCodeenum.CODE_36.value, 'CODE_36')
        self.assertEqual(AlertLevelCodeenum.CODE_43.value, 'CODE_43')
        self.assertEqual(AlertLevelCodeenum.CODE_44.value, 'CODE_44')
        self.assertEqual(AlertLevelCodeenum.CODE_45.value, 'CODE_45')
        self.assertEqual(AlertLevelCodeenum.CODE_49.value, 'CODE_49')