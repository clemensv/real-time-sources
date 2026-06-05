"""
Test case for Trips
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.trips import Trips
from gtfs_producer_data.generaltransitfeedstatic.calendar import Calendar
from gtfs_producer_data.generaltransitfeedstatic.calendardates import CalendarDates
from typing import Any


class Test_Trips(unittest.TestCase):
    """
    Test case for Trips
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Trips.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Trips for testing
        """
        instance = Trips(
            routeId='hmioewhxdatmqygvygdr',
            serviceDates=None,
            serviceExceptions=[None, None],
            tripId='rbcjfwncfwvsppnjgutm',
            tripHeadsign='elbneejbixngqxrdxaqn',
            tripShortName='copunqspolntktcatuvl',
            directionId=None,
            blockId='czjhooxmbwiprqryvzum',
            shapeId='vqpqyqoxephdhwvbfjep',
            wheelchairAccessible=None,
            bikesAllowed=None
        )
        return instance

    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'hmioewhxdatmqygvygdr'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_serviceDates_property(self):
        """
        Test serviceDates property
        """
        test_value = None
        self.instance.serviceDates = test_value
        self.assertEqual(self.instance.serviceDates, test_value)
    
    def test_serviceExceptions_property(self):
        """
        Test serviceExceptions property
        """
        test_value = [None, None]
        self.instance.serviceExceptions = test_value
        self.assertEqual(self.instance.serviceExceptions, test_value)
    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'rbcjfwncfwvsppnjgutm'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_tripHeadsign_property(self):
        """
        Test tripHeadsign property
        """
        test_value = 'elbneejbixngqxrdxaqn'
        self.instance.tripHeadsign = test_value
        self.assertEqual(self.instance.tripHeadsign, test_value)
    
    def test_tripShortName_property(self):
        """
        Test tripShortName property
        """
        test_value = 'copunqspolntktcatuvl'
        self.instance.tripShortName = test_value
        self.assertEqual(self.instance.tripShortName, test_value)
    
    def test_directionId_property(self):
        """
        Test directionId property
        """
        test_value = None
        self.instance.directionId = test_value
        self.assertEqual(self.instance.directionId, test_value)
    
    def test_blockId_property(self):
        """
        Test blockId property
        """
        test_value = 'czjhooxmbwiprqryvzum'
        self.instance.blockId = test_value
        self.assertEqual(self.instance.blockId, test_value)
    
    def test_shapeId_property(self):
        """
        Test shapeId property
        """
        test_value = 'vqpqyqoxephdhwvbfjep'
        self.instance.shapeId = test_value
        self.assertEqual(self.instance.shapeId, test_value)
    
    def test_wheelchairAccessible_property(self):
        """
        Test wheelchairAccessible property
        """
        test_value = None
        self.instance.wheelchairAccessible = test_value
        self.assertEqual(self.instance.wheelchairAccessible, test_value)
    
    def test_bikesAllowed_property(self):
        """
        Test bikesAllowed property
        """
        test_value = None
        self.instance.bikesAllowed = test_value
        self.assertEqual(self.instance.bikesAllowed, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Trips.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Trips.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

