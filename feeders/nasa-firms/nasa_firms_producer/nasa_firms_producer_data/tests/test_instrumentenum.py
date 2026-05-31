import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nasa_firms_producer_data.nasa.firms.instrumentenum import InstrumentEnum


class Test_InstrumentEnum(unittest.TestCase):
    """
    Test case for InstrumentEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = InstrumentEnum.VIIRS

    @staticmethod
    def create_instance():
        """
        Create instance of InstrumentEnum
        """
        return InstrumentEnum.VIIRS

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(InstrumentEnum.VIIRS.value, 'VIIRS')
        self.assertEqual(InstrumentEnum.MODIS.value, 'MODIS')