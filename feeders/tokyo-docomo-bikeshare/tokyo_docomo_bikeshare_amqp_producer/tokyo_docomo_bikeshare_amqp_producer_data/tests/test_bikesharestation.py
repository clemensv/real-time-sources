"""
Test case for BikeshareStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tokyo_docomo_bikeshare_amqp_producer_data.bikesharestation import BikeshareStation


class Test_BikeshareStation(unittest.TestCase):
    """
    Test case for BikeshareStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BikeshareStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BikeshareStation for testing
        """
        instance = BikeshareStation(
            system_id='jixeuachuskxqawdwthx',
            station_id='uggcnkcmnnqtqbvanwdf',
            name='foolpbdyhpaiabgdhkby',
            short_name='ykjlqffyvcmwtmwpoczl',
            lat=float(49.69321263914457),
            lon=float(27.014209420182855),
            address='vgmfieheeybkoknzlnqi',
            cross_street='ezltjwtfhcvcoqwyjdwo',
            region_id='wgxklvggitzkttjsrzxa',
            post_code='waovodomlowoqechgxel',
            capacity=int(30),
            is_virtual_station=True
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'jixeuachuskxqawdwthx'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'uggcnkcmnnqtqbvanwdf'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'foolpbdyhpaiabgdhkby'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_short_name_property(self):
        """
        Test short_name property
        """
        test_value = 'ykjlqffyvcmwtmwpoczl'
        self.instance.short_name = test_value
        self.assertEqual(self.instance.short_name, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(49.69321263914457)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(27.014209420182855)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'vgmfieheeybkoknzlnqi'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_cross_street_property(self):
        """
        Test cross_street property
        """
        test_value = 'ezltjwtfhcvcoqwyjdwo'
        self.instance.cross_street = test_value
        self.assertEqual(self.instance.cross_street, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'wgxklvggitzkttjsrzxa'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_post_code_property(self):
        """
        Test post_code property
        """
        test_value = 'waovodomlowoqechgxel'
        self.instance.post_code = test_value
        self.assertEqual(self.instance.post_code, test_value)
    
    def test_capacity_property(self):
        """
        Test capacity property
        """
        test_value = int(30)
        self.instance.capacity = test_value
        self.assertEqual(self.instance.capacity, test_value)
    
    def test_is_virtual_station_property(self):
        """
        Test is_virtual_station property
        """
        test_value = True
        self.instance.is_virtual_station = test_value
        self.assertEqual(self.instance.is_virtual_station, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BikeshareStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BikeshareStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

