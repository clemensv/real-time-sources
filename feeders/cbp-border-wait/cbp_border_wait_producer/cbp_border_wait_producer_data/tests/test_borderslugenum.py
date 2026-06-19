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
        self.instance = BorderSlugenum.canadian_MINUSborder

    @staticmethod
    def create_instance():
        """
        Create instance of BorderSlugenum
        """
        return BorderSlugenum.canadian_MINUSborder

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(BorderSlugenum.canadian_MINUSborder.value, 'canadian-border')
        self.assertEqual(BorderSlugenum.mexican_MINUSborder.value, 'mexican-border')