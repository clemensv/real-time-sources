import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicleposition_types.congestionlevel import CongestionLevel

class Test_CongestionLevel(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_CongestionLevel.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CongestionLevel
        """
        return "UNKNOWN_CONGESTION_LEVEL"
