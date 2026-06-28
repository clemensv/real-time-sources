import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_producer_data.jp.jma.amedas.observationeventenum import ObservationEventEnum


class Test_ObservationEventEnum(unittest.TestCase):
    """
    Test case for ObservationEventEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ObservationEventEnum.observation

    @staticmethod
    def create_instance():
        """
        Create instance of ObservationEventEnum
        """
        return ObservationEventEnum.observation

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ObservationEventEnum.observation.value, 'observation')