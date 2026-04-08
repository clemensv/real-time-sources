"""
Test case for PortCallAreaDetail
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.portcallareadetail import PortCallAreaDetail
import datetime


class Test_PortCallAreaDetail(unittest.TestCase):
    """
    Test case for PortCallAreaDetail
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PortCallAreaDetail.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PortCallAreaDetail for testing
        """
        instance = PortCallAreaDetail(
            port_area_code='yhqjmbxbwlkjyhqcqboq',
            port_area_name='qqnjorzutcpncawzndne',
            berth_code='mofljbdjnqsixeiwhaok',
            berth_name='gapeayzgagrwxbkthjzf',
            eta=datetime.datetime.now(datetime.timezone.utc),
            eta_source='ocnuxivwflnbzpcoqvba',
            etd=datetime.datetime.now(datetime.timezone.utc),
            etd_source='fbrinsjknujhwkjnnybg',
            ata=datetime.datetime.now(datetime.timezone.utc),
            ata_source='eioywwyytjiyeoeabcur',
            atd=datetime.datetime.now(datetime.timezone.utc),
            atd_source='droqdyvbqkpvwtyinhkp',
            arrival_draught=float(30.763836047521277),
            departure_draught=float(96.34515068123969)
        )
        return instance

    
    def test_port_area_code_property(self):
        """
        Test port_area_code property
        """
        test_value = 'yhqjmbxbwlkjyhqcqboq'
        self.instance.port_area_code = test_value
        self.assertEqual(self.instance.port_area_code, test_value)
    
    def test_port_area_name_property(self):
        """
        Test port_area_name property
        """
        test_value = 'qqnjorzutcpncawzndne'
        self.instance.port_area_name = test_value
        self.assertEqual(self.instance.port_area_name, test_value)
    
    def test_berth_code_property(self):
        """
        Test berth_code property
        """
        test_value = 'mofljbdjnqsixeiwhaok'
        self.instance.berth_code = test_value
        self.assertEqual(self.instance.berth_code, test_value)
    
    def test_berth_name_property(self):
        """
        Test berth_name property
        """
        test_value = 'gapeayzgagrwxbkthjzf'
        self.instance.berth_name = test_value
        self.assertEqual(self.instance.berth_name, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_eta_source_property(self):
        """
        Test eta_source property
        """
        test_value = 'ocnuxivwflnbzpcoqvba'
        self.instance.eta_source = test_value
        self.assertEqual(self.instance.eta_source, test_value)
    
    def test_etd_property(self):
        """
        Test etd property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.etd = test_value
        self.assertEqual(self.instance.etd, test_value)
    
    def test_etd_source_property(self):
        """
        Test etd_source property
        """
        test_value = 'fbrinsjknujhwkjnnybg'
        self.instance.etd_source = test_value
        self.assertEqual(self.instance.etd_source, test_value)
    
    def test_ata_property(self):
        """
        Test ata property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.ata = test_value
        self.assertEqual(self.instance.ata, test_value)
    
    def test_ata_source_property(self):
        """
        Test ata_source property
        """
        test_value = 'eioywwyytjiyeoeabcur'
        self.instance.ata_source = test_value
        self.assertEqual(self.instance.ata_source, test_value)
    
    def test_atd_property(self):
        """
        Test atd property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.atd = test_value
        self.assertEqual(self.instance.atd, test_value)
    
    def test_atd_source_property(self):
        """
        Test atd_source property
        """
        test_value = 'droqdyvbqkpvwtyinhkp'
        self.instance.atd_source = test_value
        self.assertEqual(self.instance.atd_source, test_value)
    
    def test_arrival_draught_property(self):
        """
        Test arrival_draught property
        """
        test_value = float(30.763836047521277)
        self.instance.arrival_draught = test_value
        self.assertEqual(self.instance.arrival_draught, test_value)
    
    def test_departure_draught_property(self):
        """
        Test departure_draught property
        """
        test_value = float(96.34515068123969)
        self.instance.departure_draught = test_value
        self.assertEqual(self.instance.departure_draught, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PortCallAreaDetail.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PortCallAreaDetail.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

