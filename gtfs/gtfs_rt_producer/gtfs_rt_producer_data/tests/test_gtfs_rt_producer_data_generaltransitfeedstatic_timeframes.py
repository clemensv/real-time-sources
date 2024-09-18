"""
Test case for Timeframes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.timeframes import Timeframes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_calendar import Test_Calendar
from test_gtfs_rt_producer_data_generaltransitfeedstatic_calendardates import Test_CalendarDates


class Test_Timeframes(unittest.TestCase):
    """
    Test case for Timeframes
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Timeframes.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Timeframes for testing
        """
        instance = Timeframes(
            timeframeGroupId='eztdcirkdgljiwpgideb',
            startTime='opgpjebgrhrkauqxxohe',
            endTime='ifartiukhxrhpcisoxga',
            serviceDates=Test_Calendar.create_instance()
        )
        return instance

    
    def test_timeframeGroupId_property(self):
        """
        Test timeframeGroupId property
        """
        test_value = 'eztdcirkdgljiwpgideb'
        self.instance.timeframeGroupId = test_value
        self.assertEqual(self.instance.timeframeGroupId, test_value)
    
    def test_startTime_property(self):
        """
        Test startTime property
        """
        test_value = 'opgpjebgrhrkauqxxohe'
        self.instance.startTime = test_value
        self.assertEqual(self.instance.startTime, test_value)
    
    def test_endTime_property(self):
        """
        Test endTime property
        """
        test_value = 'ifartiukhxrhpcisoxga'
        self.instance.endTime = test_value
        self.assertEqual(self.instance.endTime, test_value)
    
    def test_serviceDates_property(self):
        """
        Test serviceDates property
        """
        test_value = Test_Calendar.create_instance()
        self.instance.serviceDates = test_value
        self.assertEqual(self.instance.serviceDates, test_value)
    
