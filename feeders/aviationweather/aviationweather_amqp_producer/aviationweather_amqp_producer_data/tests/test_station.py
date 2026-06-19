"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aviationweather_amqp_producer_data.station import Station


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
            icao_id='ulkxkywjdwjndmgjwnsa',
            iata_id='hgkakepkqpwacdnyldqe',
            faa_id='xajbhcflxainydplqpyq',
            wmo_id='cqkuaccsxynwlvjlddxz',
            name='wsczewjkicjarfjmmheo',
            latitude=float(76.37254515601019),
            longitude=float(52.71761895842779),
            elevation=float(25.4866030571822),
            state='hspashndqicofibtgyox',
            country='lnlaofpjxhbyttqozhdg',
            site_type='adjlfprihfvjgrewfeap'
        )
        return instance

    
    def test_icao_id_property(self):
        """
        Test icao_id property
        """
        test_value = 'ulkxkywjdwjndmgjwnsa'
        self.instance.icao_id = test_value
        self.assertEqual(self.instance.icao_id, test_value)
    
    def test_iata_id_property(self):
        """
        Test iata_id property
        """
        test_value = 'hgkakepkqpwacdnyldqe'
        self.instance.iata_id = test_value
        self.assertEqual(self.instance.iata_id, test_value)
    
    def test_faa_id_property(self):
        """
        Test faa_id property
        """
        test_value = 'xajbhcflxainydplqpyq'
        self.instance.faa_id = test_value
        self.assertEqual(self.instance.faa_id, test_value)
    
    def test_wmo_id_property(self):
        """
        Test wmo_id property
        """
        test_value = 'cqkuaccsxynwlvjlddxz'
        self.instance.wmo_id = test_value
        self.assertEqual(self.instance.wmo_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wsczewjkicjarfjmmheo'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(76.37254515601019)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(52.71761895842779)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(25.4866030571822)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'hspashndqicofibtgyox'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'lnlaofpjxhbyttqozhdg'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_site_type_property(self):
        """
        Test site_type property
        """
        test_value = 'adjlfprihfvjgrewfeap'
        self.instance.site_type = test_value
        self.assertEqual(self.instance.site_type, test_value)
    
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

