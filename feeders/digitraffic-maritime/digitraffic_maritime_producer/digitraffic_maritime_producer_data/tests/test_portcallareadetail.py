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
            port_area_code='lecteywpddoznybkpngo',
            port_area_name='thezagjmolruqyuhbubk',
            berth_code='vsczmrtujglalidhpthr',
            berth_name='oqaplfxmxdovoepmmdxa',
            eta=datetime.datetime.now(datetime.timezone.utc),
            eta_source='qtgrthsrbsiviynxdchm',
            etd=datetime.datetime.now(datetime.timezone.utc),
            etd_source='oyktioqlzwtkpibbrqxf',
            ata=datetime.datetime.now(datetime.timezone.utc),
            ata_source='ulqhcijqqqvqrumsnbvs',
            atd=datetime.datetime.now(datetime.timezone.utc),
            atd_source='pbjkcaueiubtlcyyeskl',
            arrival_draught=float(95.38043293178639),
            departure_draught=float(15.685335670489675)
        )
        return instance

    
    def test_port_area_code_property(self):
        """
        Test port_area_code property
        """
        test_value = 'lecteywpddoznybkpngo'
        self.instance.port_area_code = test_value
        self.assertEqual(self.instance.port_area_code, test_value)
    
    def test_port_area_name_property(self):
        """
        Test port_area_name property
        """
        test_value = 'thezagjmolruqyuhbubk'
        self.instance.port_area_name = test_value
        self.assertEqual(self.instance.port_area_name, test_value)
    
    def test_berth_code_property(self):
        """
        Test berth_code property
        """
        test_value = 'vsczmrtujglalidhpthr'
        self.instance.berth_code = test_value
        self.assertEqual(self.instance.berth_code, test_value)
    
    def test_berth_name_property(self):
        """
        Test berth_name property
        """
        test_value = 'oqaplfxmxdovoepmmdxa'
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
        test_value = 'qtgrthsrbsiviynxdchm'
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
        test_value = 'oyktioqlzwtkpibbrqxf'
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
        test_value = 'ulqhcijqqqvqrumsnbvs'
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
        test_value = 'pbjkcaueiubtlcyyeskl'
        self.instance.atd_source = test_value
        self.assertEqual(self.instance.atd_source, test_value)
    
    def test_arrival_draught_property(self):
        """
        Test arrival_draught property
        """
        test_value = float(95.38043293178639)
        self.instance.arrival_draught = test_value
        self.assertEqual(self.instance.arrival_draught, test_value)
    
    def test_departure_draught_property(self):
        """
        Test departure_draught property
        """
        test_value = float(15.685335670489675)
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

