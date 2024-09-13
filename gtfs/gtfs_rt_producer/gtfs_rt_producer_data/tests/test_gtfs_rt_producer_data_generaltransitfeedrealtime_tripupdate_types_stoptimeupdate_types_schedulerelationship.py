import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.tripupdate_types.stoptimeupdate_types.schedulerelationship import ScheduleRelationship

class Test_ScheduleRelationship(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_ScheduleRelationship.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ScheduleRelationship
        """
        return "SCHEDULED"
