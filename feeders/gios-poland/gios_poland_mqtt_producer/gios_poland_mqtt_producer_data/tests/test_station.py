"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gios_poland_mqtt_producer_data.station import Station


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
            station_id=int(53),
            station_code='duoocisgxmcxrnjwjanp',
            name='eqlpeyyysxczqdvfshap',
            latitude=float(84.78066994071462),
            longitude=float(54.74463765098223),
            city_id=int(76),
            city_name='ztcruscldcypkqxcswkm',
            commune='vmlbipgnxoxpzyjsnzko',
            district='bujgpfjlgiwcgkohhpcn',
            voivodeship='xowepfmzeprkpidkofsr',
            street='bnnvezratbxtzpoyqthg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(53)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'duoocisgxmcxrnjwjanp'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'eqlpeyyysxczqdvfshap'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(84.78066994071462)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(54.74463765098223)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_city_id_property(self):
        """
        Test city_id property
        """
        test_value = int(76)
        self.instance.city_id = test_value
        self.assertEqual(self.instance.city_id, test_value)
    
    def test_city_name_property(self):
        """
        Test city_name property
        """
        test_value = 'ztcruscldcypkqxcswkm'
        self.instance.city_name = test_value
        self.assertEqual(self.instance.city_name, test_value)
    
    def test_commune_property(self):
        """
        Test commune property
        """
        test_value = 'vmlbipgnxoxpzyjsnzko'
        self.instance.commune = test_value
        self.assertEqual(self.instance.commune, test_value)
    
    def test_district_property(self):
        """
        Test district property
        """
        test_value = 'bujgpfjlgiwcgkohhpcn'
        self.instance.district = test_value
        self.assertEqual(self.instance.district, test_value)
    
    def test_voivodeship_property(self):
        """
        Test voivodeship property
        """
        test_value = 'xowepfmzeprkpidkofsr'
        self.instance.voivodeship = test_value
        self.assertEqual(self.instance.voivodeship, test_value)
    
    def test_street_property(self):
        """
        Test street property
        """
        test_value = 'bnnvezratbxtzpoyqthg'
        self.instance.street = test_value
        self.assertEqual(self.instance.street, test_value)
    
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

