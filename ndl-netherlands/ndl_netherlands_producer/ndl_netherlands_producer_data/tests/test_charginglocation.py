"""
Test case for ChargingLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.charginglocation import ChargingLocation
from typing import Any
from ndl_netherlands_producer_data.parkingtypeenum import ParkingTypeenum
import datetime


class Test_ChargingLocation(unittest.TestCase):
    """
    Test case for ChargingLocation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ChargingLocation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ChargingLocation for testing
        """
        instance = ChargingLocation(
            location_id='blbguhrbkzhkmqvdlcft',
            country_code='mgwtuklmnsuopbsbiswq',
            party_id='tejpzrgqvkbuvxbvfhgr',
            publish=True,
            name='gpirjksyswdqjecoxrde',
            address='kofutgvnfkloolgblexi',
            city='xgzdyxvwlqcleaeozdfb',
            postal_code='yeetlfwbfzftoejrgeum',
            state='yyrdnzahjxallsrrilpw',
            country='ibkveeeromyootirbavv',
            latitude=float(87.46895938054465),
            longitude=float(78.8595677660295),
            parking_type=ParkingTypeenum.ALONG_MOTORWAY,
            operator_name='wyotintzunvqxvqjzvep',
            operator_website='vsdsmmhxcgruptzhtnda',
            suboperator_name='aspgrlmsmwsqiqdadzso',
            owner_name='ixtbfvcogxzcvhyqbmee',
            facilities=None,
            time_zone='airzflrzgdefuqpufako',
            opening_times_twentyfourseven=False,
            charging_when_closed=True,
            energy_mix_is_green_energy=True,
            energy_mix_supplier_name='iyriupwmwabobeykglsf',
            evse_count=int(30),
            connector_count=int(20),
            last_updated=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = 'blbguhrbkzhkmqvdlcft'
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'mgwtuklmnsuopbsbiswq'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_party_id_property(self):
        """
        Test party_id property
        """
        test_value = 'tejpzrgqvkbuvxbvfhgr'
        self.instance.party_id = test_value
        self.assertEqual(self.instance.party_id, test_value)
    
    def test_publish_property(self):
        """
        Test publish property
        """
        test_value = True
        self.instance.publish = test_value
        self.assertEqual(self.instance.publish, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'gpirjksyswdqjecoxrde'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'kofutgvnfkloolgblexi'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_city_property(self):
        """
        Test city property
        """
        test_value = 'xgzdyxvwlqcleaeozdfb'
        self.instance.city = test_value
        self.assertEqual(self.instance.city, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'yeetlfwbfzftoejrgeum'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'yyrdnzahjxallsrrilpw'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'ibkveeeromyootirbavv'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(87.46895938054465)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(78.8595677660295)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_parking_type_property(self):
        """
        Test parking_type property
        """
        test_value = ParkingTypeenum.ALONG_MOTORWAY
        self.instance.parking_type = test_value
        self.assertEqual(self.instance.parking_type, test_value)
    
    def test_operator_name_property(self):
        """
        Test operator_name property
        """
        test_value = 'wyotintzunvqxvqjzvep'
        self.instance.operator_name = test_value
        self.assertEqual(self.instance.operator_name, test_value)
    
    def test_operator_website_property(self):
        """
        Test operator_website property
        """
        test_value = 'vsdsmmhxcgruptzhtnda'
        self.instance.operator_website = test_value
        self.assertEqual(self.instance.operator_website, test_value)
    
    def test_suboperator_name_property(self):
        """
        Test suboperator_name property
        """
        test_value = 'aspgrlmsmwsqiqdadzso'
        self.instance.suboperator_name = test_value
        self.assertEqual(self.instance.suboperator_name, test_value)
    
    def test_owner_name_property(self):
        """
        Test owner_name property
        """
        test_value = 'ixtbfvcogxzcvhyqbmee'
        self.instance.owner_name = test_value
        self.assertEqual(self.instance.owner_name, test_value)
    
    def test_facilities_property(self):
        """
        Test facilities property
        """
        test_value = None
        self.instance.facilities = test_value
        self.assertEqual(self.instance.facilities, test_value)
    
    def test_time_zone_property(self):
        """
        Test time_zone property
        """
        test_value = 'airzflrzgdefuqpufako'
        self.instance.time_zone = test_value
        self.assertEqual(self.instance.time_zone, test_value)
    
    def test_opening_times_twentyfourseven_property(self):
        """
        Test opening_times_twentyfourseven property
        """
        test_value = False
        self.instance.opening_times_twentyfourseven = test_value
        self.assertEqual(self.instance.opening_times_twentyfourseven, test_value)
    
    def test_charging_when_closed_property(self):
        """
        Test charging_when_closed property
        """
        test_value = True
        self.instance.charging_when_closed = test_value
        self.assertEqual(self.instance.charging_when_closed, test_value)
    
    def test_energy_mix_is_green_energy_property(self):
        """
        Test energy_mix_is_green_energy property
        """
        test_value = True
        self.instance.energy_mix_is_green_energy = test_value
        self.assertEqual(self.instance.energy_mix_is_green_energy, test_value)
    
    def test_energy_mix_supplier_name_property(self):
        """
        Test energy_mix_supplier_name property
        """
        test_value = 'iyriupwmwabobeykglsf'
        self.instance.energy_mix_supplier_name = test_value
        self.assertEqual(self.instance.energy_mix_supplier_name, test_value)
    
    def test_evse_count_property(self):
        """
        Test evse_count property
        """
        test_value = int(30)
        self.instance.evse_count = test_value
        self.assertEqual(self.instance.evse_count, test_value)
    
    def test_connector_count_property(self):
        """
        Test connector_count property
        """
        test_value = int(20)
        self.instance.connector_count = test_value
        self.assertEqual(self.instance.connector_count, test_value)
    
    def test_last_updated_property(self):
        """
        Test last_updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.last_updated = test_value
        self.assertEqual(self.instance.last_updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ChargingLocation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ChargingLocation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

