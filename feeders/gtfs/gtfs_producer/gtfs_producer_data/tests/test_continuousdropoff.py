import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.continuousdropoff import ContinuousDropOff


class Test_ContinuousDropOff(unittest.TestCase):
    """
    Test case for ContinuousDropOff
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ContinuousDropOff.CONTINUOUS_STOPPING

    @staticmethod
    def create_instance():
        """
        Create instance of ContinuousDropOff
        """
        return ContinuousDropOff.CONTINUOUS_STOPPING

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ContinuousDropOff.CONTINUOUS_STOPPING.value, 'CONTINUOUS_STOPPING')
        self.assertEqual(ContinuousDropOff.NO_CONTINUOUS_STOPPING.value, 'NO_CONTINUOUS_STOPPING')
        self.assertEqual(ContinuousDropOff.PHONE_AGENCY.value, 'PHONE_AGENCY')
        self.assertEqual(ContinuousDropOff.COORDINATE_WITH_DRIVER.value, 'COORDINATE_WITH_DRIVER')