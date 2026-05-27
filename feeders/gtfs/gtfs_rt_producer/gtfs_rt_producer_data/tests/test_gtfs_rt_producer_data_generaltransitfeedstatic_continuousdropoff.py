import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.continuousdropoff import ContinuousDropOff

class Test_ContinuousDropOff(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_ContinuousDropOff.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ContinuousDropOff
        """
        return "CONTINUOUS_STOPPING"
