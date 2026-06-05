"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bafu_hydro_producer_data.station import Station


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
            station_id='fizfgkcnsdkkwouozlsk',
            name='ymlojqoaicskqfekpcto',
            water_body_name='henmqoyqantzbokcgydl',
            water_body_type='wrkldmsjwhctylubqufp',
            latitude=float(0.3474441017899621),
            longitude=float(54.28279473230161)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fizfgkcnsdkkwouozlsk'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ymlojqoaicskqfekpcto'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_water_body_name_property(self):
        """
        Test water_body_name property
        """
        test_value = 'henmqoyqantzbokcgydl'
        self.instance.water_body_name = test_value
        self.assertEqual(self.instance.water_body_name, test_value)
    
    def test_water_body_type_property(self):
        """
        Test water_body_type property
        """
        test_value = 'wrkldmsjwhctylubqufp'
        self.instance.water_body_type = test_value
        self.assertEqual(self.instance.water_body_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(0.3474441017899621)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(54.28279473230161)
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

