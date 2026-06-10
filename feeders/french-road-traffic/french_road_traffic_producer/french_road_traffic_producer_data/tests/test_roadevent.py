"""
Test case for RoadEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent


class Test_RoadEvent(unittest.TestCase):
    """
    Test case for RoadEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RoadEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RoadEvent for testing
        """
        instance = RoadEvent(
            situation_id='vilnmxxihgeukthiygoz',
            record_id='ggrhidrfxsxtzftuxmcu',
            version='nhbbokvkxduocdytspcp',
            severity='ylvnyvbzgaqkzhszdpuv',
            record_type='jtrzmlyccbwlwoivzyud',
            probability='cgfdqzdvkuuedpkbbtcp',
            latitude=float(29.364260786573315),
            longitude=float(42.07058117453294),
            road_number='mskvkiuizqexjgxgqjda',
            town_name='pjosdnimfhosbucuxett',
            direction='igzxwfzcqhclwridbhbv',
            description='fzrojjwulteacijknefy',
            location_description='cquticcekovrthmrhaom',
            source_name='wgahlthbhtjsrraaquzf',
            validity_status='ecnvmcerbbucsyvpmjzf',
            overall_start_time='sbsihotpwswtcfsgayyx',
            overall_end_time='rdmdyyiyncocwlnjlcje',
            creation_time='nkcqkorkmgzlsqvelzif',
            observation_time='nvjgfvmhfseqleolgjoo'
        )
        return instance

    
    def test_situation_id_property(self):
        """
        Test situation_id property
        """
        test_value = 'vilnmxxihgeukthiygoz'
        self.instance.situation_id = test_value
        self.assertEqual(self.instance.situation_id, test_value)
    
    def test_record_id_property(self):
        """
        Test record_id property
        """
        test_value = 'ggrhidrfxsxtzftuxmcu'
        self.instance.record_id = test_value
        self.assertEqual(self.instance.record_id, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = 'nhbbokvkxduocdytspcp'
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'ylvnyvbzgaqkzhszdpuv'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_record_type_property(self):
        """
        Test record_type property
        """
        test_value = 'jtrzmlyccbwlwoivzyud'
        self.instance.record_type = test_value
        self.assertEqual(self.instance.record_type, test_value)
    
    def test_probability_property(self):
        """
        Test probability property
        """
        test_value = 'cgfdqzdvkuuedpkbbtcp'
        self.instance.probability = test_value
        self.assertEqual(self.instance.probability, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(29.364260786573315)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(42.07058117453294)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = 'mskvkiuizqexjgxgqjda'
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_town_name_property(self):
        """
        Test town_name property
        """
        test_value = 'pjosdnimfhosbucuxett'
        self.instance.town_name = test_value
        self.assertEqual(self.instance.town_name, test_value)
    
    def test_direction_property(self):
        """
        Test direction property
        """
        test_value = 'igzxwfzcqhclwridbhbv'
        self.instance.direction = test_value
        self.assertEqual(self.instance.direction, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'fzrojjwulteacijknefy'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'cquticcekovrthmrhaom'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_source_name_property(self):
        """
        Test source_name property
        """
        test_value = 'wgahlthbhtjsrraaquzf'
        self.instance.source_name = test_value
        self.assertEqual(self.instance.source_name, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'ecnvmcerbbucsyvpmjzf'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_overall_start_time_property(self):
        """
        Test overall_start_time property
        """
        test_value = 'sbsihotpwswtcfsgayyx'
        self.instance.overall_start_time = test_value
        self.assertEqual(self.instance.overall_start_time, test_value)
    
    def test_overall_end_time_property(self):
        """
        Test overall_end_time property
        """
        test_value = 'rdmdyyiyncocwlnjlcje'
        self.instance.overall_end_time = test_value
        self.assertEqual(self.instance.overall_end_time, test_value)
    
    def test_creation_time_property(self):
        """
        Test creation_time property
        """
        test_value = 'nkcqkorkmgzlsqvelzif'
        self.instance.creation_time = test_value
        self.assertEqual(self.instance.creation_time, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'nvjgfvmhfseqleolgjoo'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RoadEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RoadEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

