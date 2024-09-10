"""
Test case for FeedHeader
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.feedheader import FeedHeader
from test_gtfs_rt_producer_data_generaltransitfeed_feedheader_types_incrementality import Test_Incrementality

class Test_FeedHeader(unittest.TestCase):
    """
    Test case for FeedHeader
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedHeader.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedHeader for testing
        """
        instance = FeedHeader(
            gtfs_realtime_version='hgodojmmjgcvyifsihep',
            incrementality=Test_Incrementality.create_instance(),
            timestamp=int(34)
        )
        return instance

    
    def test_gtfs_realtime_version_property(self):
        """
        Test gtfs_realtime_version property
        """
        test_value = 'hgodojmmjgcvyifsihep'
        self.instance.gtfs_realtime_version = test_value
        self.assertEqual(self.instance.gtfs_realtime_version, test_value)
    
    def test_incrementality_property(self):
        """
        Test incrementality property
        """
        test_value = Test_Incrementality.create_instance()
        self.instance.incrementality = test_value
        self.assertEqual(self.instance.incrementality, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(34)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
