"""
Test case for StationBoard
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_amqp_producer_data.be.irail.stationboard import StationBoard
from irail_amqp_producer_data.be.irail.departure import Departure


class Test_StationBoard(unittest.TestCase):
    """
    Test case for StationBoard
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationBoard.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationBoard for testing
        """
        instance = StationBoard(
            station_id='nnkdhphqpaorkahrqaed',
            station_name='kadvqmluhmhfotnajzez',
            retrieved_at='nbqgrebhipdwkfyvzysl',
            departure_count=int(89),
            departures=[None]
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nnkdhphqpaorkahrqaed'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'kadvqmluhmhfotnajzez'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_retrieved_at_property(self):
        """
        Test retrieved_at property
        """
        test_value = 'nbqgrebhipdwkfyvzysl'
        self.instance.retrieved_at = test_value
        self.assertEqual(self.instance.retrieved_at, test_value)
    
    def test_departure_count_property(self):
        """
        Test departure_count property
        """
        test_value = int(89)
        self.instance.departure_count = test_value
        self.assertEqual(self.instance.departure_count, test_value)
    
    def test_departures_property(self):
        """
        Test departures property
        """
        test_value = [None]
        self.instance.departures = test_value
        self.assertEqual(self.instance.departures, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationBoard.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationBoard.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

