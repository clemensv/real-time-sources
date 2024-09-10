import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.continuouspickup import ContinuousPickup

class Test_ContinuousPickup(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_ContinuousPickup.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ContinuousPickup
        """
        return "CONTINUOUS_STOPPING"
