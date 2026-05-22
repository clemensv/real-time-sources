"""
Test case for TidewaterStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.tidewaterstation import TidewaterStation


class Test_TidewaterStation(unittest.TestCase):
    """
    Test case for TidewaterStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TidewaterStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TidewaterStation for testing
        """
        instance = TidewaterStation(
            station_id='iimfnixknjgfsnzvoybc',
            name='ifumndghowzvgoqkrapr',
            country='axmmdmadvlttjwjfybro',
            owner='xkqmckjwsesrqrjnetgq',
            latitude=float(79.48011949251406),
            longitude=float(87.62942771974154),
            valid_from='mpvynbuhrcnlelycvxfz',
            valid_to='ahvhlbhvoynqxayivgpl'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'iimfnixknjgfsnzvoybc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ifumndghowzvgoqkrapr'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'axmmdmadvlttjwjfybro'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'xkqmckjwsesrqrjnetgq'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(79.48011949251406)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(87.62942771974154)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_valid_from_property(self):
        """
        Test valid_from property
        """
        test_value = 'mpvynbuhrcnlelycvxfz'
        self.instance.valid_from = test_value
        self.assertEqual(self.instance.valid_from, test_value)
    
    def test_valid_to_property(self):
        """
        Test valid_to property
        """
        test_value = 'ahvhlbhvoynqxayivgpl'
        self.instance.valid_to = test_value
        self.assertEqual(self.instance.valid_to, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TidewaterStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TidewaterStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

