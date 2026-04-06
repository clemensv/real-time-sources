"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from syke_hydro_producer_data.station import Station


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
            station_id='cuzwpwljwufcxznhpmnx',
            name='xkcisoybqdqzdapvfkqz',
            river_name='cnynatgdjlzbbycjmqai',
            water_area_name='jbgychzutmnkicvkrnwv',
            municipality='zsogwxanalrzhcqsziku',
            latitude=float(69.80134621013381),
            longitude=float(32.36669655870931)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'cuzwpwljwufcxznhpmnx'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xkcisoybqdqzdapvfkqz'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'cnynatgdjlzbbycjmqai'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_water_area_name_property(self):
        """
        Test water_area_name property
        """
        test_value = 'jbgychzutmnkicvkrnwv'
        self.instance.water_area_name = test_value
        self.assertEqual(self.instance.water_area_name, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'zsogwxanalrzhcqsziku'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(69.80134621013381)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(32.36669655870931)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
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

