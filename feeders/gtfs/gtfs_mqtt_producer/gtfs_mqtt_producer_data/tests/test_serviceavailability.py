import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.serviceavailability import ServiceAvailability


class Test_ServiceAvailability(unittest.TestCase):
    """
    Test case for ServiceAvailability
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ServiceAvailability.NO_SERVICE

    @staticmethod
    def create_instance():
        """
        Create instance of ServiceAvailability
        """
        return ServiceAvailability.NO_SERVICE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ServiceAvailability.NO_SERVICE.value, 'NO_SERVICE')
        self.assertEqual(ServiceAvailability.SERVICE_AVAILABLE.value, 'SERVICE_AVAILABLE')