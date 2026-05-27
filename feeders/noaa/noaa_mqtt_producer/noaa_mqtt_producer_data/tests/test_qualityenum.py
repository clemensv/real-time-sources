import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_mqtt_producer_data.microsoft.opendata.us.noaa.qualityenum import QualityEnum


class Test_QualityEnum(unittest.TestCase):
    """
    Test case for QualityEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = QualityEnum.Preliminary

    @staticmethod
    def create_instance():
        """
        Create instance of QualityEnum
        """
        return QualityEnum.Preliminary

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(QualityEnum.Preliminary.value, 'Preliminary')
        self.assertEqual(QualityEnum.Verified.value, 'Verified')