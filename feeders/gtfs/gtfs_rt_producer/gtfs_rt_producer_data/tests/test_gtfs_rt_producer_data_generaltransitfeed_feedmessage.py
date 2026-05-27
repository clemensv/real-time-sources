"""
Test case for FeedMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.feedmessage import FeedMessage
from test_gtfs_rt_producer_data_generaltransitfeed_feedheader import Test_FeedHeader
from test_gtfs_rt_producer_data_generaltransitfeed_feedentity import Test_FeedEntity

class Test_FeedMessage(unittest.TestCase):
    """
    Test case for FeedMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedMessage for testing
        """
        instance = FeedMessage(
            header=Test_FeedHeader.create_instance(),
            entity=[Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance()]
        )
        return instance

    
    def test_header_property(self):
        """
        Test header property
        """
        test_value = Test_FeedHeader.create_instance()
        self.instance.header = test_value
        self.assertEqual(self.instance.header, test_value)
    
    def test_entity_property(self):
        """
        Test entity property
        """
        test_value = [Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance(), Test_FeedEntity.create_instance()]
        self.instance.entity = test_value
        self.assertEqual(self.instance.entity, test_value)
    
