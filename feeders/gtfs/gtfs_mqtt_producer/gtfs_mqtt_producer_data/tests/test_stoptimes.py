"""
Test case for StopTimes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.stoptimes import StopTimes
from typing import Any


class Test_StopTimes(unittest.TestCase):
    """
    Test case for StopTimes
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StopTimes.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StopTimes for testing
        """
        instance = StopTimes(
            tripId='vhkjjexptiszjvtqvzcc',
            arrivalTime='yfobtvbpnkxemnynpdgr',
            departureTime='djlkqctdjjglmqjvlhlv',
            stopId='gqdtsntrnxsuhewalgkf',
            stopSequence=int(57),
            stopHeadsign='lkyjmhbslufcskexncue',
            pickupType=None,
            dropOffType=None,
            continuousPickup=None,
            continuousDropOff=None,
            shapeDistTraveled=float(52.028000055035285),
            timepoint=None
        )
        return instance

    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'vhkjjexptiszjvtqvzcc'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_arrivalTime_property(self):
        """
        Test arrivalTime property
        """
        test_value = 'yfobtvbpnkxemnynpdgr'
        self.instance.arrivalTime = test_value
        self.assertEqual(self.instance.arrivalTime, test_value)
    
    def test_departureTime_property(self):
        """
        Test departureTime property
        """
        test_value = 'djlkqctdjjglmqjvlhlv'
        self.instance.departureTime = test_value
        self.assertEqual(self.instance.departureTime, test_value)
    
    def test_stopId_property(self):
        """
        Test stopId property
        """
        test_value = 'gqdtsntrnxsuhewalgkf'
        self.instance.stopId = test_value
        self.assertEqual(self.instance.stopId, test_value)
    
    def test_stopSequence_property(self):
        """
        Test stopSequence property
        """
        test_value = int(57)
        self.instance.stopSequence = test_value
        self.assertEqual(self.instance.stopSequence, test_value)
    
    def test_stopHeadsign_property(self):
        """
        Test stopHeadsign property
        """
        test_value = 'lkyjmhbslufcskexncue'
        self.instance.stopHeadsign = test_value
        self.assertEqual(self.instance.stopHeadsign, test_value)
    
    def test_pickupType_property(self):
        """
        Test pickupType property
        """
        test_value = None
        self.instance.pickupType = test_value
        self.assertEqual(self.instance.pickupType, test_value)
    
    def test_dropOffType_property(self):
        """
        Test dropOffType property
        """
        test_value = None
        self.instance.dropOffType = test_value
        self.assertEqual(self.instance.dropOffType, test_value)
    
    def test_continuousPickup_property(self):
        """
        Test continuousPickup property
        """
        test_value = None
        self.instance.continuousPickup = test_value
        self.assertEqual(self.instance.continuousPickup, test_value)
    
    def test_continuousDropOff_property(self):
        """
        Test continuousDropOff property
        """
        test_value = None
        self.instance.continuousDropOff = test_value
        self.assertEqual(self.instance.continuousDropOff, test_value)
    
    def test_shapeDistTraveled_property(self):
        """
        Test shapeDistTraveled property
        """
        test_value = float(52.028000055035285)
        self.instance.shapeDistTraveled = test_value
        self.assertEqual(self.instance.shapeDistTraveled, test_value)
    
    def test_timepoint_property(self):
        """
        Test timepoint property
        """
        test_value = None
        self.instance.timepoint = test_value
        self.assertEqual(self.instance.timepoint, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StopTimes.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StopTimes.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

