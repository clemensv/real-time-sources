"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from snotel_producer_data.station import Station


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
            station_triplet='cldsstqewcaatzougzhr',
            name='uenryxtczejxdwvokwfy',
            state='ebkzpkicahdpozxsyfza',
            elevation=float(89.21259004747989),
            latitude=float(49.45301832705914),
            longitude=float(70.42106268672774)
        )
        return instance

    
    def test_station_triplet_property(self):
        """
        Test station_triplet property
        """
        test_value = 'cldsstqewcaatzougzhr'
        self.instance.station_triplet = test_value
        self.assertEqual(self.instance.station_triplet, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'uenryxtczejxdwvokwfy'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'ebkzpkicahdpozxsyfza'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(89.21259004747989)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(49.45301832705914)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(70.42106268672774)
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

