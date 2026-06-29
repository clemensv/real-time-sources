import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.hfp.temporaltypeenum import TemporalTypeEnum


class Test_TemporalTypeEnum(unittest.TestCase):
    """
    Test case for TemporalTypeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TemporalTypeEnum.ongoing

    @staticmethod
    def create_instance():
        """
        Create instance of TemporalTypeEnum
        """
        return TemporalTypeEnum.ongoing

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TemporalTypeEnum.ongoing.value, 'ongoing')
        self.assertEqual(TemporalTypeEnum.upcoming.value, 'upcoming')