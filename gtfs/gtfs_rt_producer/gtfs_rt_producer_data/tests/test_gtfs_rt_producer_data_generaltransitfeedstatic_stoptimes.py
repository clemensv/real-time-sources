"""
Test case for StopTimes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.stoptimes import StopTimes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_continuousdropoff import Test_ContinuousDropOff
from test_gtfs_rt_producer_data_generaltransitfeedstatic_continuouspickup import Test_ContinuousPickup
from test_gtfs_rt_producer_data_generaltransitfeedstatic_dropofftype import Test_DropOffType
from test_gtfs_rt_producer_data_generaltransitfeedstatic_pickuptype import Test_PickupType
from test_gtfs_rt_producer_data_generaltransitfeedstatic_timepoint import Test_Timepoint


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
            tripId='jjyjtxkchdlatngekwfj',
            arrivalTime='lejbyvpooisaqqsouarc',
            departureTime='vgwttgjsgswszklfwgwv',
            stopId='ondfgcyxkoyorajkxkcm',
            stopSequence=int(24),
            stopHeadsign='tiuxjpyuvbdohslvrmeg',
            pickupType=Test_PickupType.create_instance(),
            dropOffType=Test_DropOffType.create_instance(),
            continuousPickup=Test_ContinuousPickup.create_instance(),
            continuousDropOff=Test_ContinuousDropOff.create_instance(),
            shapeDistTraveled=float(37.71752954838713),
            timepoint=Test_Timepoint.create_instance()
        )
        return instance

    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'jjyjtxkchdlatngekwfj'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_arrivalTime_property(self):
        """
        Test arrivalTime property
        """
        test_value = 'lejbyvpooisaqqsouarc'
        self.instance.arrivalTime = test_value
        self.assertEqual(self.instance.arrivalTime, test_value)
    
    def test_departureTime_property(self):
        """
        Test departureTime property
        """
        test_value = 'vgwttgjsgswszklfwgwv'
        self.instance.departureTime = test_value
        self.assertEqual(self.instance.departureTime, test_value)
    
    def test_stopId_property(self):
        """
        Test stopId property
        """
        test_value = 'ondfgcyxkoyorajkxkcm'
        self.instance.stopId = test_value
        self.assertEqual(self.instance.stopId, test_value)
    
    def test_stopSequence_property(self):
        """
        Test stopSequence property
        """
        test_value = int(24)
        self.instance.stopSequence = test_value
        self.assertEqual(self.instance.stopSequence, test_value)
    
    def test_stopHeadsign_property(self):
        """
        Test stopHeadsign property
        """
        test_value = 'tiuxjpyuvbdohslvrmeg'
        self.instance.stopHeadsign = test_value
        self.assertEqual(self.instance.stopHeadsign, test_value)
    
    def test_pickupType_property(self):
        """
        Test pickupType property
        """
        test_value = Test_PickupType.create_instance()
        self.instance.pickupType = test_value
        self.assertEqual(self.instance.pickupType, test_value)
    
    def test_dropOffType_property(self):
        """
        Test dropOffType property
        """
        test_value = Test_DropOffType.create_instance()
        self.instance.dropOffType = test_value
        self.assertEqual(self.instance.dropOffType, test_value)
    
    def test_continuousPickup_property(self):
        """
        Test continuousPickup property
        """
        test_value = Test_ContinuousPickup.create_instance()
        self.instance.continuousPickup = test_value
        self.assertEqual(self.instance.continuousPickup, test_value)
    
    def test_continuousDropOff_property(self):
        """
        Test continuousDropOff property
        """
        test_value = Test_ContinuousDropOff.create_instance()
        self.instance.continuousDropOff = test_value
        self.assertEqual(self.instance.continuousDropOff, test_value)
    
    def test_shapeDistTraveled_property(self):
        """
        Test shapeDistTraveled property
        """
        test_value = float(37.71752954838713)
        self.instance.shapeDistTraveled = test_value
        self.assertEqual(self.instance.shapeDistTraveled, test_value)
    
    def test_timepoint_property(self):
        """
        Test timepoint property
        """
        test_value = Test_Timepoint.create_instance()
        self.instance.timepoint = test_value
        self.assertEqual(self.instance.timepoint, test_value)
    
