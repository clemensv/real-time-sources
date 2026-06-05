"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from environment_canada_amqp_producer_data.station import Station


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
            msc_id='zaxkguwowvirpietdgur',
            name='sayjrvdlcwdezfvwtooc',
            iata_id='qfqdzeyqbtyvogtgkaqg',
            wmo_id=int(1),
            province_territory='nevfqgptuwjdkwiuqhbl',
            data_provider='faevbcblyrlofdwtzgdd',
            dataset_network='ombssrlivvrlkcxzcmuf',
            auto_man='ugslezkudzevieqoxmpv',
            latitude=float(11.11126205737676),
            longitude=float(68.19120071075116),
            elevation=float(50.16640097674539),
            province='bhbgmfarvfjamjpagdpn'
        )
        return instance

    
    def test_msc_id_property(self):
        """
        Test msc_id property
        """
        test_value = 'zaxkguwowvirpietdgur'
        self.instance.msc_id = test_value
        self.assertEqual(self.instance.msc_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'sayjrvdlcwdezfvwtooc'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_iata_id_property(self):
        """
        Test iata_id property
        """
        test_value = 'qfqdzeyqbtyvogtgkaqg'
        self.instance.iata_id = test_value
        self.assertEqual(self.instance.iata_id, test_value)
    
    def test_wmo_id_property(self):
        """
        Test wmo_id property
        """
        test_value = int(1)
        self.instance.wmo_id = test_value
        self.assertEqual(self.instance.wmo_id, test_value)
    
    def test_province_territory_property(self):
        """
        Test province_territory property
        """
        test_value = 'nevfqgptuwjdkwiuqhbl'
        self.instance.province_territory = test_value
        self.assertEqual(self.instance.province_territory, test_value)
    
    def test_data_provider_property(self):
        """
        Test data_provider property
        """
        test_value = 'faevbcblyrlofdwtzgdd'
        self.instance.data_provider = test_value
        self.assertEqual(self.instance.data_provider, test_value)
    
    def test_dataset_network_property(self):
        """
        Test dataset_network property
        """
        test_value = 'ombssrlivvrlkcxzcmuf'
        self.instance.dataset_network = test_value
        self.assertEqual(self.instance.dataset_network, test_value)
    
    def test_auto_man_property(self):
        """
        Test auto_man property
        """
        test_value = 'ugslezkudzevieqoxmpv'
        self.instance.auto_man = test_value
        self.assertEqual(self.instance.auto_man, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(11.11126205737676)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(68.19120071075116)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(50.16640097674539)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'bhbgmfarvfjamjpagdpn'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
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

