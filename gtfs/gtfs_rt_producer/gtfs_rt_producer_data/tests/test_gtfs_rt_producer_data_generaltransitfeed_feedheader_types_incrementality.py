import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.feedheader_types.incrementality import Incrementality

class Test_Incrementality(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_Incrementality.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Incrementality
        """
        return "FULL_DATASET"
