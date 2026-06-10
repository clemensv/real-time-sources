"""
Test case for TemporarySpeedLimit
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_mqtt_producer_data.temporaryspeedlimit import TemporarySpeedLimit


class Test_TemporarySpeedLimit(unittest.TestCase):
    """
    Test case for TemporarySpeedLimit
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TemporarySpeedLimit.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TemporarySpeedLimit for testing
        """
        instance = TemporarySpeedLimit(
            situation_record_id='ymjqfzombvdzdoormsmg',
            version_time='iktaefycfbsrflcvzluu',
            validity_status='eazaoxxymraqvbbpwoen',
            start_time='niolizqreeucxzyvonsg',
            end_time='mbneacxmolcmralsjbyh',
            road_name='fskvdodkdksutvzwdmop',
            speed_limit_kmh=int(59),
            description='srnrhqwqnmgwaasmlqvx',
            location_description='tvorerrkuezvrkfpdzei'
        )
        return instance

    
    def test_situation_record_id_property(self):
        """
        Test situation_record_id property
        """
        test_value = 'ymjqfzombvdzdoormsmg'
        self.instance.situation_record_id = test_value
        self.assertEqual(self.instance.situation_record_id, test_value)
    
    def test_version_time_property(self):
        """
        Test version_time property
        """
        test_value = 'iktaefycfbsrflcvzluu'
        self.instance.version_time = test_value
        self.assertEqual(self.instance.version_time, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'eazaoxxymraqvbbpwoen'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'niolizqreeucxzyvonsg'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'mbneacxmolcmralsjbyh'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'fskvdodkdksutvzwdmop'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_speed_limit_kmh_property(self):
        """
        Test speed_limit_kmh property
        """
        test_value = int(59)
        self.instance.speed_limit_kmh = test_value
        self.assertEqual(self.instance.speed_limit_kmh, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'srnrhqwqnmgwaasmlqvx'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'tvorerrkuezvrkfpdzei'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TemporarySpeedLimit.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TemporarySpeedLimit.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

