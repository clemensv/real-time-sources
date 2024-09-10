import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.serviceavailability import ServiceAvailability

class Test_ServiceAvailability(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_ServiceAvailability.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ServiceAvailability
        """
        return "NO_SERVICE"
