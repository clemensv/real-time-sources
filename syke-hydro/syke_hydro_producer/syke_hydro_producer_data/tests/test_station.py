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
            station_id='vqnqaydaugvtorvhhdrx',
            name='yoojsykbvokvlldkokfv',
            river_name='tavgwwzfnbljbgyhqntu',
            water_area_name='bngehixojaujtthkypta',
            municipality='nrcvwvmgcoyhvllrhduh',
            latitude=float(63.21382821995015),
            longitude=float(18.51679693765015)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vqnqaydaugvtorvhhdrx'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'yoojsykbvokvlldkokfv'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'tavgwwzfnbljbgyhqntu'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_water_area_name_property(self):
        """
        Test water_area_name property
        """
        test_value = 'bngehixojaujtthkypta'
        self.instance.water_area_name = test_value
        self.assertEqual(self.instance.water_area_name, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'nrcvwvmgcoyhvllrhduh'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(63.21382821995015)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(18.51679693765015)
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

