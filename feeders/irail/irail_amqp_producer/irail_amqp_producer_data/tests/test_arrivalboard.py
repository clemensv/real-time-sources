"""
Test case for ArrivalBoard
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_amqp_producer_data.be.irail.arrivalboard import ArrivalBoard
from irail_amqp_producer_data.be.irail.arrival import Arrival


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
            station_id='ufpwtnrexmrcpaamcbeb',
            station_name='kxjbdnvkuumhcrwyiwhr',
            retrieved_at='qdanhbiqsfliozwqcuui',
            arrival_count=int(89),
            arrivals=[None]
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ufpwtnrexmrcpaamcbeb'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'kxjbdnvkuumhcrwyiwhr'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_retrieved_at_property(self):
        """
        Test retrieved_at property
        """
        test_value = 'qdanhbiqsfliozwqcuui'
        self.instance.retrieved_at = test_value
        self.assertEqual(self.instance.retrieved_at, test_value)
    
    def test_arrival_count_property(self):
        """
        Test arrival_count property
        """
        test_value = int(89)
        self.instance.arrival_count = test_value
        self.assertEqual(self.instance.arrival_count, test_value)
    
    def test_arrivals_property(self):
        """
        Test arrivals property
        """
        test_value = [None]
        self.instance.arrivals = test_value
        self.assertEqual(self.instance.arrivals, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ArrivalBoard.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ArrivalBoard.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

