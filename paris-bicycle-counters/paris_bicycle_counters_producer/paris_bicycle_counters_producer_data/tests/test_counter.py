"""
Test case for Counter
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from paris_bicycle_counters_producer_data.counter import Counter


class Test_Counter(unittest.TestCase):
    """
    Test case for Counter
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Counter.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Counter for testing
        """
        instance = Counter(
            counter_id='zrvsuonysmaswvbqmose',
            counter_name='fclazqmxyyspakcisqia',
            channel_name='gcsnutqetqsxdvkkiznr',
            installation_date='slvtubgdetkczyehvqbz',
            longitude=float(56.00297718770655),
            latitude=float(40.88633319343566)
        )
        return instance

    
    def test_counter_id_property(self):
        """
        Test counter_id property
        """
        test_value = 'zrvsuonysmaswvbqmose'
        self.instance.counter_id = test_value
        self.assertEqual(self.instance.counter_id, test_value)
    
    def test_counter_name_property(self):
        """
        Test counter_name property
        """
        test_value = 'fclazqmxyyspakcisqia'
        self.instance.counter_name = test_value
        self.assertEqual(self.instance.counter_name, test_value)
    
    def test_channel_name_property(self):
        """
        Test channel_name property
        """
        test_value = 'gcsnutqetqsxdvkkiznr'
        self.instance.channel_name = test_value
        self.assertEqual(self.instance.channel_name, test_value)
    
    def test_installation_date_property(self):
        """
        Test installation_date property
        """
        test_value = 'slvtubgdetkczyehvqbz'
        self.instance.installation_date = test_value
        self.assertEqual(self.instance.installation_date, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(56.00297718770655)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(40.88633319343566)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Counter.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Counter.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

