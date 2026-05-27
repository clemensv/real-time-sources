import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.alert.alert_types.cause import Cause


class Test_Cause(unittest.TestCase):
    """
    Test case for Cause
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = Cause.UNKNOWN_CAUSE

    @staticmethod
    def create_instance():
        """
        Create instance of Cause
        """
        return Cause.UNKNOWN_CAUSE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(Cause.UNKNOWN_CAUSE.value, 'UNKNOWN_CAUSE')
        self.assertEqual(Cause.OTHER_CAUSE.value, 'OTHER_CAUSE')
        self.assertEqual(Cause.TECHNICAL_PROBLEM.value, 'TECHNICAL_PROBLEM')
        self.assertEqual(Cause.STRIKE.value, 'STRIKE')
        self.assertEqual(Cause.DEMONSTRATION.value, 'DEMONSTRATION')
        self.assertEqual(Cause.ACCIDENT.value, 'ACCIDENT')
        self.assertEqual(Cause.HOLIDAY.value, 'HOLIDAY')
        self.assertEqual(Cause.WEATHER.value, 'WEATHER')
        self.assertEqual(Cause.MAINTENANCE.value, 'MAINTENANCE')
        self.assertEqual(Cause.CONSTRUCTION.value, 'CONSTRUCTION')
        self.assertEqual(Cause.POLICE_ACTIVITY.value, 'POLICE_ACTIVITY')
        self.assertEqual(Cause.MEDICAL_EMERGENCY.value, 'MEDICAL_EMERGENCY')