"""
Test case for ArrivalBoard
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_producer_data.be.irail.arrivalboard import ArrivalBoard
from test_irail_producer_data_be_irail_arrival import Test_Arrival


class Test_ArrivalBoard(unittest.TestCase):
    """
    Test case for ArrivalBoard
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ArrivalBoard.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ArrivalBoard for testing
        """
        instance = ArrivalBoard(
            station_id='vvursykterltnpbafpcn',
            station_name='rqoqustzdwjmpregrlae',
            retrieved_at='cyvbtgguvsfbrhlqtciy',
            arrival_count=int(6),
            arrivals=[Test_Arrival.create_instance(), Test_Arrival.create_instance(), Test_Arrival.create_instance(), Test_Arrival.create_instance()]
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vvursykterltnpbafpcn'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'rqoqustzdwjmpregrlae'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_retrieved_at_property(self):
        """
        Test retrieved_at property
        """
        test_value = 'cyvbtgguvsfbrhlqtciy'
        self.instance.retrieved_at = test_value
        self.assertEqual(self.instance.retrieved_at, test_value)
    
    def test_arrival_count_property(self):
        """
        Test arrival_count property
        """
        test_value = int(6)
        self.instance.arrival_count = test_value
        self.assertEqual(self.instance.arrival_count, test_value)
    
    def test_arrivals_property(self):
        """
        Test arrivals property
        """
        test_value = [Test_Arrival.create_instance(), Test_Arrival.create_instance(), Test_Arrival.create_instance(), Test_Arrival.create_instance()]
        self.instance.arrivals = test_value
        self.assertEqual(self.instance.arrivals, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ArrivalBoard.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
