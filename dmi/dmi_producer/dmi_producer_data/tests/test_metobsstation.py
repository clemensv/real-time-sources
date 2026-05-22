"""
Test case for MetObsStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.metobsstation import MetObsStation


class Test_MetObsStation(unittest.TestCase):
    """
    Test case for MetObsStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MetObsStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MetObsStation for testing
        """
        instance = MetObsStation(
            station_id='ucufzskxxbjzasavnjbd',
            wmo_station_id='fyaupfpaijrefztlkbsv',
            wmo_country_code='qjhiiodinsaxpshlowlx',
            name='xtkorvgypftjwvxgvjmf',
            country='hqtbsxybijepydkzpbzr',
            owner='mbsthafnntdntewlazqo',
            region_id='awymtufkupjgwkzaawfc',
            type='fjywhcalxnttymwhmnmh',
            status='ehdsaccguwbtejeygwxa',
            parameter_id=['ljnxzbeojacdhjfcgkco', 'jtljenfniqzfwvfabmny', 'zknvaxazavkbfkrjrglh', 'eqwijxtnbitkyhpfgxii'],
            latitude=float(26.717665369122656),
            longitude=float(44.9890222143601),
            station_height=float(92.87611330390226),
            barometer_height=float(30.84244164035126),
            anemometer_height=float(26.787822701252274),
            valid_from='rqtsaalnoitnbqgqrvaj',
            valid_to='sdchpsdogjrzgoajvtje',
            operation_from='hxevahgadshhfeshvjig',
            operation_to='iqfmnlxwuhtluftxzaju',
            created='osyavlevwymuxdpjzpnn',
            updated='vhfwxyjlxklyodtomjov'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ucufzskxxbjzasavnjbd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_wmo_station_id_property(self):
        """
        Test wmo_station_id property
        """
        test_value = 'fyaupfpaijrefztlkbsv'
        self.instance.wmo_station_id = test_value
        self.assertEqual(self.instance.wmo_station_id, test_value)
    
    def test_wmo_country_code_property(self):
        """
        Test wmo_country_code property
        """
        test_value = 'qjhiiodinsaxpshlowlx'
        self.instance.wmo_country_code = test_value
        self.assertEqual(self.instance.wmo_country_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xtkorvgypftjwvxgvjmf'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'hqtbsxybijepydkzpbzr'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'mbsthafnntdntewlazqo'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'awymtufkupjgwkzaawfc'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'fjywhcalxnttymwhmnmh'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'ehdsaccguwbtejeygwxa'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = ['ljnxzbeojacdhjfcgkco', 'jtljenfniqzfwvfabmny', 'zknvaxazavkbfkrjrglh', 'eqwijxtnbitkyhpfgxii']
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(26.717665369122656)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(44.9890222143601)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_station_height_property(self):
        """
        Test station_height property
        """
        test_value = float(92.87611330390226)
        self.instance.station_height = test_value
        self.assertEqual(self.instance.station_height, test_value)
    
    def test_barometer_height_property(self):
        """
        Test barometer_height property
        """
        test_value = float(30.84244164035126)
        self.instance.barometer_height = test_value
        self.assertEqual(self.instance.barometer_height, test_value)
    
    def test_anemometer_height_property(self):
        """
        Test anemometer_height property
        """
        test_value = float(26.787822701252274)
        self.instance.anemometer_height = test_value
        self.assertEqual(self.instance.anemometer_height, test_value)
    
    def test_valid_from_property(self):
        """
        Test valid_from property
        """
        test_value = 'rqtsaalnoitnbqgqrvaj'
        self.instance.valid_from = test_value
        self.assertEqual(self.instance.valid_from, test_value)
    
    def test_valid_to_property(self):
        """
        Test valid_to property
        """
        test_value = 'sdchpsdogjrzgoajvtje'
        self.instance.valid_to = test_value
        self.assertEqual(self.instance.valid_to, test_value)
    
    def test_operation_from_property(self):
        """
        Test operation_from property
        """
        test_value = 'hxevahgadshhfeshvjig'
        self.instance.operation_from = test_value
        self.assertEqual(self.instance.operation_from, test_value)
    
    def test_operation_to_property(self):
        """
        Test operation_to property
        """
        test_value = 'iqfmnlxwuhtluftxzaju'
        self.instance.operation_to = test_value
        self.assertEqual(self.instance.operation_to, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'osyavlevwymuxdpjzpnn'
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'vhfwxyjlxklyodtomjov'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MetObsStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MetObsStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

