import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.timepoint import Timepoint


class Test_Timepoint(unittest.TestCase):
    """
    Test case for Timepoint
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = Timepoint.APPROXIMATE

    @staticmethod
    def create_instance():
        """
        Create instance of Timepoint
        """
        return Timepoint.APPROXIMATE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(Timepoint.APPROXIMATE.value, 'APPROXIMATE')
        self.assertEqual(Timepoint.EXACT.value, 'EXACT')