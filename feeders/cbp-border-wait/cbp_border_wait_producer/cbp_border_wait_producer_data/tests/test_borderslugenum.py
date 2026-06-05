import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cbp_border_wait_producer_data.gov.cbp.borderwait.borderslugenum import BorderSlugenum


class Test_BorderSlugenum(unittest.TestCase):
    """
    Test case for BorderSlugenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = BorderSlugenum.canadian_border

    @staticmethod
    def create_instance():
        """
        Create instance of BorderSlugenum
        """
        return BorderSlugenum.canadian_border

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(BorderSlugenum.canadian_border.value, 'canadian-border')
        self.assertEqual(BorderSlugenum.mexican_border.value, 'mexican-border')