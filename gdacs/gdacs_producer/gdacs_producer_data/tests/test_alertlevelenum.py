import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gdacs_producer_data.alertlevelenum import AlertLevelenum


class Test_AlertLevelenum(unittest.TestCase):
    """
    Test case for AlertLevelenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = AlertLevelenum.Green

    @staticmethod
    def create_instance():
        """
        Create instance of AlertLevelenum
        """
        return AlertLevelenum.Green

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(AlertLevelenum.Green.value, "Green")
        self.assertEqual(AlertLevelenum.Orange.value, "Orange")
        self.assertEqual(AlertLevelenum.Red.value, "Red")