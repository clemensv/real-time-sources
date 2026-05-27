import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.directionid import DirectionId


class Test_DirectionId(unittest.TestCase):
    """
    Test case for DirectionId
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = DirectionId.OUTBOUND

    @staticmethod
    def create_instance():
        """
        Create instance of DirectionId
        """
        return DirectionId.OUTBOUND

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(DirectionId.OUTBOUND.value, 'OUTBOUND')
        self.assertEqual(DirectionId.INBOUND.value, 'INBOUND')