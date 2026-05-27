import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_mqtt_producer_data.microsoft.opendata.us.noaa.qualitylevel import QualityLevel


class Test_QualityLevel(unittest.TestCase):
    """
    Test case for QualityLevel
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = QualityLevel.Preliminary

    @staticmethod
    def create_instance():
        """
        Create instance of QualityLevel
        """
        return QualityLevel.Preliminary

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(QualityLevel.Preliminary.value, 'Preliminary')
        self.assertEqual(QualityLevel.Verified.value, 'Verified')