"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from waterinfo_vmm_producer_data.station import Station


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
            station_no='oslbxglhkrmpftnszzos',
            station_name='fficmpcmthbeswntsnef',
            station_id='csgamctobyngdvumlzyw',
            station_latitude=float(51.18002921847869),
            station_longitude=float(79.49768578312327),
            river_name='ndvkyqdlofgesvwkkzwc',
            stationparameter_name='hsnxrgaglygkvaarmajc',
            ts_id='exgwlgpjqlwyxhbhycxo',
            ts_unitname='iagbdeqevggqklfwvlxy',
            water_body='iegxxnfhertabxhqkcno'
        )
        return instance

    
    def test_station_no_property(self):
        """
        Test station_no property
        """
        test_value = 'oslbxglhkrmpftnszzos'
        self.instance.station_no = test_value
        self.assertEqual(self.instance.station_no, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'fficmpcmthbeswntsnef'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'csgamctobyngdvumlzyw'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_latitude_property(self):
        """
        Test station_latitude property
        """
        test_value = float(51.18002921847869)
        self.instance.station_latitude = test_value
        self.assertEqual(self.instance.station_latitude, test_value)
    
    def test_station_longitude_property(self):
        """
        Test station_longitude property
        """
        test_value = float(79.49768578312327)
        self.instance.station_longitude = test_value
        self.assertEqual(self.instance.station_longitude, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'ndvkyqdlofgesvwkkzwc'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_stationparameter_name_property(self):
        """
        Test stationparameter_name property
        """
        test_value = 'hsnxrgaglygkvaarmajc'
        self.instance.stationparameter_name = test_value
        self.assertEqual(self.instance.stationparameter_name, test_value)
    
    def test_ts_id_property(self):
        """
        Test ts_id property
        """
        test_value = 'exgwlgpjqlwyxhbhycxo'
        self.instance.ts_id = test_value
        self.assertEqual(self.instance.ts_id, test_value)
    
    def test_ts_unitname_property(self):
        """
        Test ts_unitname property
        """
        test_value = 'iagbdeqevggqklfwvlxy'
        self.instance.ts_unitname = test_value
        self.assertEqual(self.instance.ts_unitname, test_value)
    
    def test_water_body_property(self):
        """
        Test water_body property
        """
        test_value = 'iegxxnfhertabxhqkcno'
        self.instance.water_body = test_value
        self.assertEqual(self.instance.water_body, test_value)
    
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

