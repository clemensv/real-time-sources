import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_producer_data.displaytypeenum import DisplayTypeenum


class Test_DisplayTypeenum(unittest.TestCase):
    """
    Test case for DisplayTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = DisplayTypeenum.ROADWORKS

    @staticmethod
    def create_instance():
        """
        Create instance of DisplayTypeenum
        """
        return DisplayTypeenum.ROADWORKS

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(DisplayTypeenum.ROADWORKS.value, "ROADWORKS")
        self.assertEqual(DisplayTypeenum.SHORT_TERM_ROADWORKS.value, "SHORT_TERM_ROADWORKS")
        self.assertEqual(DisplayTypeenum.CLOSURE.value, "CLOSURE")
        self.assertEqual(DisplayTypeenum.CLOSURE_ENTRY_EXIT.value, "CLOSURE_ENTRY_EXIT")
        self.assertEqual(DisplayTypeenum.WEIGHT_LIMIT_35.value, "WEIGHT_LIMIT_35")