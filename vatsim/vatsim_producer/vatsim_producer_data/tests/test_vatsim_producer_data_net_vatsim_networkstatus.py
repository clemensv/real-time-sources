"""
Test case for NetworkStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from vatsim_producer_data.net.vatsim.networkstatus import NetworkStatus
import datetime


class Test_NetworkStatus(unittest.TestCase):
    """
    Test case for NetworkStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_NetworkStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of NetworkStatus for testing
        """
        instance = NetworkStatus(
            callsign='xzopunqcmtwnzydxbxxz',
            update_timestamp=datetime.datetime.now(datetime.timezone.utc),
            connected_clients=int(2),
            unique_users=int(60),
            pilot_count=int(30),
            controller_count=int(64)
        )
        return instance

    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'xzopunqcmtwnzydxbxxz'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_update_timestamp_property(self):
        """
        Test update_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.update_timestamp = test_value
        self.assertEqual(self.instance.update_timestamp, test_value)
    
    def test_connected_clients_property(self):
        """
        Test connected_clients property
        """
        test_value = int(2)
        self.instance.connected_clients = test_value
        self.assertEqual(self.instance.connected_clients, test_value)
    
    def test_unique_users_property(self):
        """
        Test unique_users property
        """
        test_value = int(60)
        self.instance.unique_users = test_value
        self.assertEqual(self.instance.unique_users, test_value)
    
    def test_pilot_count_property(self):
        """
        Test pilot_count property
        """
        test_value = int(30)
        self.instance.pilot_count = test_value
        self.assertEqual(self.instance.pilot_count, test_value)
    
    def test_controller_count_property(self):
        """
        Test controller_count property
        """
        test_value = int(64)
        self.instance.controller_count = test_value
        self.assertEqual(self.instance.controller_count, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = NetworkStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
