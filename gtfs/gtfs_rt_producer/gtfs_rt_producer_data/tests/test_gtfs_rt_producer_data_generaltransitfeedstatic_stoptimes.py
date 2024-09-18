"""
Test case for StopTimes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.stoptimes import StopTimes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_timepoint import Test_Timepoint
from test_gtfs_rt_producer_data_generaltransitfeedstatic_pickuptype import Test_PickupType
from test_gtfs_rt_producer_data_generaltransitfeedstatic_continuousdropoff import Test_ContinuousDropOff
from test_gtfs_rt_producer_data_generaltransitfeedstatic_dropofftype import Test_DropOffType
from test_gtfs_rt_producer_data_generaltransitfeedstatic_continuouspickup import Test_ContinuousPickup


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
            tripId='ksotvevphvayhopfrtac',
            arrivalTime='ebiucpzumxeccfeyrila',
            departureTime='cfxsnvlfkmqnvnvzcdkh',
            stopId='vpaxomwrwkceaermperi',
            stopSequence=int(34),
            stopHeadsign='nyqpyjrycfpfzppniptj',
            pickupType=Test_PickupType.create_instance(),
            dropOffType=Test_DropOffType.create_instance(),
            continuousPickup=Test_ContinuousPickup.create_instance(),
            continuousDropOff=Test_ContinuousDropOff.create_instance(),
            shapeDistTraveled=float(23.959564066857787),
            timepoint=Test_Timepoint.create_instance()
        )
        return instance

    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'ksotvevphvayhopfrtac'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_arrivalTime_property(self):
        """
        Test arrivalTime property
        """
        test_value = 'ebiucpzumxeccfeyrila'
        self.instance.arrivalTime = test_value
        self.assertEqual(self.instance.arrivalTime, test_value)
    
    def test_departureTime_property(self):
        """
        Test departureTime property
        """
        test_value = 'cfxsnvlfkmqnvnvzcdkh'
        self.instance.departureTime = test_value
        self.assertEqual(self.instance.departureTime, test_value)
    
    def test_stopId_property(self):
        """
        Test stopId property
        """
        test_value = 'vpaxomwrwkceaermperi'
        self.instance.stopId = test_value
        self.assertEqual(self.instance.stopId, test_value)
    
    def test_stopSequence_property(self):
        """
        Test stopSequence property
        """
        test_value = int(34)
        self.instance.stopSequence = test_value
        self.assertEqual(self.instance.stopSequence, test_value)
    
    def test_stopHeadsign_property(self):
        """
        Test stopHeadsign property
        """
        test_value = 'nyqpyjrycfpfzppniptj'
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
        test_value = float(23.959564066857787)
        self.instance.shapeDistTraveled = test_value
        self.assertEqual(self.instance.shapeDistTraveled, test_value)
    
    def test_timepoint_property(self):
        """
        Test timepoint property
        """
        test_value = Test_Timepoint.create_instance()
        self.instance.timepoint = test_value
        self.assertEqual(self.instance.timepoint, test_value)
    
