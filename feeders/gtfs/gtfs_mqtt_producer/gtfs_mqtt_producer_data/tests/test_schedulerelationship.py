import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedrealtime.alert.tripdescriptor_types.schedulerelationship import ScheduleRelationship


class Test_ScheduleRelationship(unittest.TestCase):
    """
    Test case for ScheduleRelationship
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ScheduleRelationship.SCHEDULED

    @staticmethod
    def create_instance():
        """
        Create instance of ScheduleRelationship
        """
        return ScheduleRelationship.SCHEDULED

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ScheduleRelationship.SCHEDULED.value, 'SCHEDULED')
        self.assertEqual(ScheduleRelationship.ADDED.value, 'ADDED')
        self.assertEqual(ScheduleRelationship.UNSCHEDULED.value, 'UNSCHEDULED')
        self.assertEqual(ScheduleRelationship.CANCELED.value, 'CANCELED')