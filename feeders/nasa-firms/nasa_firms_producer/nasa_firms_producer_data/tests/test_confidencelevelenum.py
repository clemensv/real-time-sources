import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nasa_firms_producer_data.nasa.firms.confidencelevelenum import ConfidenceLevelenum


class Test_ConfidenceLevelenum(unittest.TestCase):
    """
    Test case for ConfidenceLevelenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ConfidenceLevelenum.low

    @staticmethod
    def create_instance():
        """
        Create instance of ConfidenceLevelenum
        """
        return ConfidenceLevelenum.low

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ConfidenceLevelenum.low.value, 'low')
        self.assertEqual(ConfidenceLevelenum.nominal.value, 'nominal')
        self.assertEqual(ConfidenceLevelenum.high.value, 'high')