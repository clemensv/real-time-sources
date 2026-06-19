"""
Test case for TemporaryClosure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.temporaryclosure import TemporaryClosure


class Test_TemporaryClosure(unittest.TestCase):
    """
    Test case for TemporaryClosure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TemporaryClosure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TemporaryClosure for testing
        """
        instance = TemporaryClosure(
            situation_record_id='ylhbpjufyubgykgttzam',
            version_time='mjyjarwrywzqqighihfa',
            validity_status='hoyamosnjsmifxlagjsa',
            start_time='jkwbwznmdsdofxbkkcri',
            end_time='fmxjtugfljawhiuzrqrq',
            road_name='egkxsalmfncaxbszrrjk',
            description='wagffffgsmkyohtacywn',
            location_description='uninkyjwemhqweylpkup',
            severity='ptspktqfjfmgcgcrdpgz'
        )
        return instance

    
    def test_situation_record_id_property(self):
        """
        Test situation_record_id property
        """
        test_value = 'ylhbpjufyubgykgttzam'
        self.instance.situation_record_id = test_value
        self.assertEqual(self.instance.situation_record_id, test_value)
    
    def test_version_time_property(self):
        """
        Test version_time property
        """
        test_value = 'mjyjarwrywzqqighihfa'
        self.instance.version_time = test_value
        self.assertEqual(self.instance.version_time, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'hoyamosnjsmifxlagjsa'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'jkwbwznmdsdofxbkkcri'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'fmxjtugfljawhiuzrqrq'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'egkxsalmfncaxbszrrjk'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'wagffffgsmkyohtacywn'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'uninkyjwemhqweylpkup'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'ptspktqfjfmgcgcrdpgz'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TemporaryClosure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TemporaryClosure.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

