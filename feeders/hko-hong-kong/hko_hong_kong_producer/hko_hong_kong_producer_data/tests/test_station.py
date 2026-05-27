"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hko_hong_kong_producer_data.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            place_id='xscugzlxaqxpxxbukddf',
            name='unmguxxocjajjrucgerj',
            data_types='zdjokaivcogkegybrhpp'
        )
        return instance

    
    def test_place_id_property(self):
        """
        Test place_id property
        """
        test_value = 'xscugzlxaqxpxxbukddf'
        self.instance.place_id = test_value
        self.assertEqual(self.instance.place_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'unmguxxocjajjrucgerj'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_data_types_property(self):
        """
        Test data_types property
        """
        test_value = 'zdjokaivcogkegybrhpp'
        self.instance.data_types = test_value
        self.assertEqual(self.instance.data_types, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

