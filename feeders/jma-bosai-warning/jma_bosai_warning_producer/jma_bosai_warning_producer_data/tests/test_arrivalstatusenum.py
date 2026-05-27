import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.arrivalstatusenum import ArrivalStatusenum


class Test_ArrivalStatusenum(unittest.TestCase):
    """
    Test case for ArrivalStatusenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ArrivalStatusenum.ESTIMATED

    @staticmethod
    def create_instance():
        """
        Create instance of ArrivalStatusenum
        """
        return ArrivalStatusenum.ESTIMATED

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ArrivalStatusenum.ESTIMATED.value, 'ESTIMATED')
        self.assertEqual(ArrivalStatusenum.FIRST_WAVE_OBSERVED.value, 'FIRST_WAVE_OBSERVED')
        self.assertEqual(ArrivalStatusenum.MAX_WAVE_OBSERVED.value, 'MAX_WAVE_OBSERVED')