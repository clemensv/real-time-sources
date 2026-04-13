"""
Test case for BridgeOpening
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.bridgeopening import BridgeOpening


class Test_BridgeOpening(unittest.TestCase):
    """
    Test case for BridgeOpening
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BridgeOpening.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BridgeOpening for testing
        """
        instance = BridgeOpening(
            situation_record_id='efnmmrpplzxvtllyoltz',
            version_time='udkhrsvprbtuhafwdnij',
            validity_status='cushsvnwdskhjwyriscu',
            start_time='xmdwjzkqbgvnyntbcjfy',
            end_time='irlmqpysqmowmbrukpes',
            bridge_name='lqwmdclqmsrvvxexvqgd',
            road_name='tocgepcqftsjwtzvhemi',
            description='fcwgvihacmfwqifljvyd'
        )
        return instance

    
    def test_situation_record_id_property(self):
        """
        Test situation_record_id property
        """
        test_value = 'efnmmrpplzxvtllyoltz'
        self.instance.situation_record_id = test_value
        self.assertEqual(self.instance.situation_record_id, test_value)
    
    def test_version_time_property(self):
        """
        Test version_time property
        """
        test_value = 'udkhrsvprbtuhafwdnij'
        self.instance.version_time = test_value
        self.assertEqual(self.instance.version_time, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'cushsvnwdskhjwyriscu'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'xmdwjzkqbgvnyntbcjfy'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'irlmqpysqmowmbrukpes'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_bridge_name_property(self):
        """
        Test bridge_name property
        """
        test_value = 'lqwmdclqmsrvvxexvqgd'
        self.instance.bridge_name = test_value
        self.assertEqual(self.instance.bridge_name, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'tocgepcqftsjwtzvhemi'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'fcwgvihacmfwqifljvyd'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BridgeOpening.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BridgeOpening.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

