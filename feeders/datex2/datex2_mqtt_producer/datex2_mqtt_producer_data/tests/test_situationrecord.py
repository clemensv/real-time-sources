"""
Test case for SituationRecord
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from datex2_mqtt_producer_data.org.datex2.situation.situationrecord import SituationRecord
import datetime


class Test_SituationRecord(unittest.TestCase):
    """
    Test case for SituationRecord
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SituationRecord.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SituationRecord for testing
        """
        instance = SituationRecord(
            supplier_id='nzoajpozzdtkunwtxhzh',
            situation_id='rdsdoknqajhwrososaku',
            situation_record_id='raimfwyqvornafpgbirt',
            feed_url='hpvpobajxhydbwzeszdf',
            version='gcvfskbohgxklsuzubvs',
            record_type='pfenjdlmvnflkyzrlhts',
            severity='ofecvjtxjsyuzfvaneev',
            probability='dbcsskfgkzrkqynvigej',
            validity_status='mwgsqpjjjzuuxfnmquvi',
            creation_time=datetime.datetime.now(datetime.timezone.utc),
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            overall_start_time=datetime.datetime.now(datetime.timezone.utc),
            overall_end_time=datetime.datetime.now(datetime.timezone.utc),
            latitude=float(80.79358562528928),
            longitude=float(93.86704512216087),
            road_number='qjutwxtzodjlitinagvl',
            direction='upmtuqyqkyxmxohxvmol',
            location_description='mjtfifijrqpdcszmbcyn',
            description='nmfgumdchzwmitwadkpo',
            source_name='ssensiqvuftxqafwzxxe',
            cause='plptwdresmhdjfxdaysl',
            management_type='rlkwbweqpyossnrkdgjt',
            raw_record='tikakwknffavjskhrmbc',
            country_code='iwuaopzmhbbmlzjudwko',
            operator_id='emztxcibltggkzhiutxb'
        )
        return instance

    
    def test_supplier_id_property(self):
        """
        Test supplier_id property
        """
        test_value = 'nzoajpozzdtkunwtxhzh'
        self.instance.supplier_id = test_value
        self.assertEqual(self.instance.supplier_id, test_value)
    
    def test_situation_id_property(self):
        """
        Test situation_id property
        """
        test_value = 'rdsdoknqajhwrososaku'
        self.instance.situation_id = test_value
        self.assertEqual(self.instance.situation_id, test_value)
    
    def test_situation_record_id_property(self):
        """
        Test situation_record_id property
        """
        test_value = 'raimfwyqvornafpgbirt'
        self.instance.situation_record_id = test_value
        self.assertEqual(self.instance.situation_record_id, test_value)
    
    def test_feed_url_property(self):
        """
        Test feed_url property
        """
        test_value = 'hpvpobajxhydbwzeszdf'
        self.instance.feed_url = test_value
        self.assertEqual(self.instance.feed_url, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = 'gcvfskbohgxklsuzubvs'
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_record_type_property(self):
        """
        Test record_type property
        """
        test_value = 'pfenjdlmvnflkyzrlhts'
        self.instance.record_type = test_value
        self.assertEqual(self.instance.record_type, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'ofecvjtxjsyuzfvaneev'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_probability_property(self):
        """
        Test probability property
        """
        test_value = 'dbcsskfgkzrkqynvigej'
        self.instance.probability = test_value
        self.assertEqual(self.instance.probability, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'mwgsqpjjjzuuxfnmquvi'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_creation_time_property(self):
        """
        Test creation_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.creation_time = test_value
        self.assertEqual(self.instance.creation_time, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_overall_start_time_property(self):
        """
        Test overall_start_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.overall_start_time = test_value
        self.assertEqual(self.instance.overall_start_time, test_value)
    
    def test_overall_end_time_property(self):
        """
        Test overall_end_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.overall_end_time = test_value
        self.assertEqual(self.instance.overall_end_time, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(80.79358562528928)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(93.86704512216087)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = 'qjutwxtzodjlitinagvl'
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_direction_property(self):
        """
        Test direction property
        """
        test_value = 'upmtuqyqkyxmxohxvmol'
        self.instance.direction = test_value
        self.assertEqual(self.instance.direction, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'mjtfifijrqpdcszmbcyn'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'nmfgumdchzwmitwadkpo'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_source_name_property(self):
        """
        Test source_name property
        """
        test_value = 'ssensiqvuftxqafwzxxe'
        self.instance.source_name = test_value
        self.assertEqual(self.instance.source_name, test_value)
    
    def test_cause_property(self):
        """
        Test cause property
        """
        test_value = 'plptwdresmhdjfxdaysl'
        self.instance.cause = test_value
        self.assertEqual(self.instance.cause, test_value)
    
    def test_management_type_property(self):
        """
        Test management_type property
        """
        test_value = 'rlkwbweqpyossnrkdgjt'
        self.instance.management_type = test_value
        self.assertEqual(self.instance.management_type, test_value)
    
    def test_raw_record_property(self):
        """
        Test raw_record property
        """
        test_value = 'tikakwknffavjskhrmbc'
        self.instance.raw_record = test_value
        self.assertEqual(self.instance.raw_record, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'iwuaopzmhbbmlzjudwko'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'emztxcibltggkzhiutxb'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SituationRecord.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SituationRecord.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

