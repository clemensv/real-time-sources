"""
Test case for TimeRange
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.timerange import TimeRange


class Test_TimeRange(unittest.TestCase):
    """
    Test case for TimeRange
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TimeRange.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TimeRange for testing
        """
        instance = TimeRange(
            start=int(24),
            end=int(42)
        )
        return instance

    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = int(24)
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = int(42)
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
