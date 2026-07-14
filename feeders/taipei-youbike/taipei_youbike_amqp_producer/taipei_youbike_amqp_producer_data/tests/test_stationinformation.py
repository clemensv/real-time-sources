"""
Test case for StationInformation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from taipei_youbike_amqp_producer_data.tw.youbike.stationinformation import StationInformation


class Test_StationInformation(unittest.TestCase):
    """
    Test case for StationInformation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationInformation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationInformation for testing
        """
        instance = StationInformation(
            station_id='zqvnaeyoisogcfqypfrd',
            name_tw='fezboiwjxwmmebybsexm',
            name_en='adsapxoxrlcbcywcgoyz',
            name_cn='lkzvkqxrdtmwrbkabpnl',
            district_tw='kabdosqfgzuclecdxvuj',
            district_en='zfcxklzsilusorhptdhd',
            district_cn='qrlngmnkpkmulmmacaak',
            address_tw='mlzkugcstiashcjrtmlr',
            address_en='eqqkonnhdcseachmnwia',
            address_cn='jojeggmtpxhsbpygfvvl',
            lat=float(16.754200224628015),
            lon=float(11.923907960439895),
            capacity=int(45),
            station_type=int(30),
            country_code='orqabouppqkqztphvhxe',
            area_code='fdzvtygykxrauhwhxrco',
            img='rcetydkksmnplwdazxtv'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zqvnaeyoisogcfqypfrd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_tw_property(self):
        """
        Test name_tw property
        """
        test_value = 'fezboiwjxwmmebybsexm'
        self.instance.name_tw = test_value
        self.assertEqual(self.instance.name_tw, test_value)
    
    def test_name_en_property(self):
        """
        Test name_en property
        """
        test_value = 'adsapxoxrlcbcywcgoyz'
        self.instance.name_en = test_value
        self.assertEqual(self.instance.name_en, test_value)
    
    def test_name_cn_property(self):
        """
        Test name_cn property
        """
        test_value = 'lkzvkqxrdtmwrbkabpnl'
        self.instance.name_cn = test_value
        self.assertEqual(self.instance.name_cn, test_value)
    
    def test_district_tw_property(self):
        """
        Test district_tw property
        """
        test_value = 'kabdosqfgzuclecdxvuj'
        self.instance.district_tw = test_value
        self.assertEqual(self.instance.district_tw, test_value)
    
    def test_district_en_property(self):
        """
        Test district_en property
        """
        test_value = 'zfcxklzsilusorhptdhd'
        self.instance.district_en = test_value
        self.assertEqual(self.instance.district_en, test_value)
    
    def test_district_cn_property(self):
        """
        Test district_cn property
        """
        test_value = 'qrlngmnkpkmulmmacaak'
        self.instance.district_cn = test_value
        self.assertEqual(self.instance.district_cn, test_value)
    
    def test_address_tw_property(self):
        """
        Test address_tw property
        """
        test_value = 'mlzkugcstiashcjrtmlr'
        self.instance.address_tw = test_value
        self.assertEqual(self.instance.address_tw, test_value)
    
    def test_address_en_property(self):
        """
        Test address_en property
        """
        test_value = 'eqqkonnhdcseachmnwia'
        self.instance.address_en = test_value
        self.assertEqual(self.instance.address_en, test_value)
    
    def test_address_cn_property(self):
        """
        Test address_cn property
        """
        test_value = 'jojeggmtpxhsbpygfvvl'
        self.instance.address_cn = test_value
        self.assertEqual(self.instance.address_cn, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(16.754200224628015)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(11.923907960439895)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_capacity_property(self):
        """
        Test capacity property
        """
        test_value = int(45)
        self.instance.capacity = test_value
        self.assertEqual(self.instance.capacity, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = int(30)
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'orqabouppqkqztphvhxe'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'fdzvtygykxrauhwhxrco'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_img_property(self):
        """
        Test img property
        """
        test_value = 'rcetydkksmnplwdazxtv'
        self.instance.img = test_value
        self.assertEqual(self.instance.img, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationInformation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationInformation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

