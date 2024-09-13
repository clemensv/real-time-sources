import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.vehiclestopstatus import VehicleStopStatus

class Test_VehicleStopStatus(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_VehicleStopStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VehicleStopStatus
        """
        return "INCOMING_AT"
