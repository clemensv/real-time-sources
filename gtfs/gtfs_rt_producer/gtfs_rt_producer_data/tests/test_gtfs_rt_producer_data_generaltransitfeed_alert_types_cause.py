import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.alert_types.cause import Cause

class Test_Cause(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_Cause.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Cause
        """
        return "UNKNOWN_CAUSE"
