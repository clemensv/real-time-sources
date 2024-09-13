import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicleposition_types.occupancystatus import OccupancyStatus

class Test_OccupancyStatus(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_OccupancyStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OccupancyStatus
        """
        return "EMPTY"
