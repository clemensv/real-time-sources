"""
Test case for Frequencies
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.frequencies import Frequencies


class Test_Frequencies(unittest.TestCase):
    """
    Test case for Frequencies
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Frequencies.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Frequencies for testing
        """
        instance = Frequencies(
            tripId='nhaftuemuzyvelvzjirb',
            startTime='ptrahrnzsurxnupnwoet',
            endTime='ieavuschuococrcpimnk',
            headwaySecs=int(53),
            exactTimes=int(100)
        )
        return instance

    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'nhaftuemuzyvelvzjirb'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_startTime_property(self):
        """
        Test startTime property
        """
        test_value = 'ptrahrnzsurxnupnwoet'
        self.instance.startTime = test_value
        self.assertEqual(self.instance.startTime, test_value)
    
    def test_endTime_property(self):
        """
        Test endTime property
        """
        test_value = 'ieavuschuococrcpimnk'
        self.instance.endTime = test_value
        self.assertEqual(self.instance.endTime, test_value)
    
    def test_headwaySecs_property(self):
        """
        Test headwaySecs property
        """
        test_value = int(53)
        self.instance.headwaySecs = test_value
        self.assertEqual(self.instance.headwaySecs, test_value)
    
    def test_exactTimes_property(self):
        """
        Test exactTimes property
        """
        test_value = int(100)
        self.instance.exactTimes = test_value
        self.assertEqual(self.instance.exactTimes, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Frequencies.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Frequencies.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

