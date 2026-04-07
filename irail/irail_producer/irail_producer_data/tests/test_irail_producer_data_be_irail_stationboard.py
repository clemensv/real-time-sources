"""
Test case for StationBoard
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_producer_data.be.irail.stationboard import StationBoard
from test_irail_producer_data_be_irail_departure import Test_Departure


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
            station_id='jltdgpdyzoysgvdcgsnj',
            station_name='ctsmroeqcfxrwhzozhai',
            retrieved_at='ydawbsatqzysqtnenjnk',
            departure_count=int(63),
            departures=[Test_Departure.create_instance(), Test_Departure.create_instance()]
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'jltdgpdyzoysgvdcgsnj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'ctsmroeqcfxrwhzozhai'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_retrieved_at_property(self):
        """
        Test retrieved_at property
        """
        test_value = 'ydawbsatqzysqtnenjnk'
        self.instance.retrieved_at = test_value
        self.assertEqual(self.instance.retrieved_at, test_value)
    
    def test_departure_count_property(self):
        """
        Test departure_count property
        """
        test_value = int(63)
        self.instance.departure_count = test_value
        self.assertEqual(self.instance.departure_count, test_value)
    
    def test_departures_property(self):
        """
        Test departures property
        """
        test_value = [Test_Departure.create_instance(), Test_Departure.create_instance()]
        self.instance.departures = test_value
        self.assertEqual(self.instance.departures, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationBoard.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
