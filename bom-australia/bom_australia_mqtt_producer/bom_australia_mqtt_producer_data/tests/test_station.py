"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bom_australia_mqtt_producer_data.station import Station


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
            station_wmo='pezuuunwvftxzupbccax',
            name='zewnpfpjestlgfzexdkg',
            product_id='tcfbjzcmppkgzxsfmguh',
            state='iwlhgohjzabwipvzfkby',
            time_zone='pzpkpqadagcyghghiwuh',
            latitude=float(69.32884377543887),
            longitude=float(5.703437557703051)
        )
        return instance

    
    def test_station_wmo_property(self):
        """
        Test station_wmo property
        """
        test_value = 'pezuuunwvftxzupbccax'
        self.instance.station_wmo = test_value
        self.assertEqual(self.instance.station_wmo, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'zewnpfpjestlgfzexdkg'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_product_id_property(self):
        """
        Test product_id property
        """
        test_value = 'tcfbjzcmppkgzxsfmguh'
        self.instance.product_id = test_value
        self.assertEqual(self.instance.product_id, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'iwlhgohjzabwipvzfkby'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_time_zone_property(self):
        """
        Test time_zone property
        """
        test_value = 'pzpkpqadagcyghghiwuh'
        self.instance.time_zone = test_value
        self.assertEqual(self.instance.time_zone, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(69.32884377543887)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(5.703437557703051)
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

