import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.timepoint import Timepoint

class Test_Timepoint(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_Timepoint.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Timepoint
        """
        return "APPROXIMATE"
