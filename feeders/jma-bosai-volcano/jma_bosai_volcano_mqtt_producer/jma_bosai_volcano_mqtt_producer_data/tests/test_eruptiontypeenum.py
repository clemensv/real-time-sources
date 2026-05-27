import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_mqtt_producer_data.eruptiontypeenum import EruptionTypeenum


class Test_EruptionTypeenum(unittest.TestCase):
    """
    Test case for EruptionTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = EruptionTypeenum.ERUPTION

    @staticmethod
    def create_instance():
        """
        Create instance of EruptionTypeenum
        """
        return EruptionTypeenum.ERUPTION

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(EruptionTypeenum.ERUPTION.value, 'ERUPTION')
        self.assertEqual(EruptionTypeenum.EXPLOSION.value, 'EXPLOSION')
        self.assertEqual(EruptionTypeenum.CONTINUOUS_ERUPTION_CONTINUING.value, 'CONTINUOUS_ERUPTION_CONTINUING')
        self.assertEqual(EruptionTypeenum.CONTINUOUS_ERUPTION_STOPPED.value, 'CONTINUOUS_ERUPTION_STOPPED')
        self.assertEqual(EruptionTypeenum.UNKNOWN.value, 'UNKNOWN')