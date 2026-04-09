"""
Test case for ReplicationState
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wikimedia_osm_diffs_producer_data.replicationstate import ReplicationState
import datetime


class Test_ReplicationState(unittest.TestCase):
    """
    Test case for ReplicationState
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ReplicationState.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ReplicationState for testing
        """
        instance = ReplicationState(
            sequence_number=int(62),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_sequence_number_property(self):
        """
        Test sequence_number property
        """
        test_value = int(62)
        self.instance.sequence_number = test_value
        self.assertEqual(self.instance.sequence_number, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ReplicationState.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ReplicationState.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

