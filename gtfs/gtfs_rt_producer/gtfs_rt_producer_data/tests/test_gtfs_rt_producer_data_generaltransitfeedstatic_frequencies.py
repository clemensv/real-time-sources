"""
Test case for Frequencies
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.frequencies import Frequencies


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
            tripId='tahijtyzhterzxhdlbmf',
            startTime='ahschhvooidibfqhildr',
            endTime='oygqtmhizzhkyadtoftx',
            headwaySecs=int(81),
            exactTimes=int(33)
        )
        return instance

    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'tahijtyzhterzxhdlbmf'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_startTime_property(self):
        """
        Test startTime property
        """
        test_value = 'ahschhvooidibfqhildr'
        self.instance.startTime = test_value
        self.assertEqual(self.instance.startTime, test_value)
    
    def test_endTime_property(self):
        """
        Test endTime property
        """
        test_value = 'oygqtmhizzhkyadtoftx'
        self.instance.endTime = test_value
        self.assertEqual(self.instance.endTime, test_value)
    
    def test_headwaySecs_property(self):
        """
        Test headwaySecs property
        """
        test_value = int(81)
        self.instance.headwaySecs = test_value
        self.assertEqual(self.instance.headwaySecs, test_value)
    
    def test_exactTimes_property(self):
        """
        Test exactTimes property
        """
        test_value = int(33)
        self.instance.exactTimes = test_value
        self.assertEqual(self.instance.exactTimes, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Frequencies.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
