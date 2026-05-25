import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_producer_data.uk.kcl.laqn.indexsourceenum import IndexSourceenum


class Test_IndexSourceenum(unittest.TestCase):
    """
    Test case for IndexSourceenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = IndexSourceenum.Measurement

    @staticmethod
    def create_instance():
        """
        Create instance of IndexSourceenum
        """
        return IndexSourceenum.Measurement

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(IndexSourceenum.Measurement.value, 'Measurement')
        self.assertEqual(IndexSourceenum.Forecast.value, 'Forecast')