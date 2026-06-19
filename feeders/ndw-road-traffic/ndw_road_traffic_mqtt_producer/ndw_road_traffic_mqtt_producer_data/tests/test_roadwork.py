"""
Test case for Roadwork
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_mqtt_producer_data.roadwork import Roadwork


class Test_Roadwork(unittest.TestCase):
    """
    Test case for Roadwork
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Roadwork.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Roadwork for testing
        """
        instance = Roadwork(
            situation_record_id='hcxzvnialkkixhpkqmue',
            version_time='wwetcximvzpqpiztaseo',
            validity_status='sdyueolcqkwvrlmpjivp',
            start_time='zwngshkdjmltkphsjlnf',
            end_time='mwocqsqhmuyxqoucrcmt',
            road_name='ojwhlgdfddqavenknwcy',
            description='fbhwfzbvuczfrqvtuezf',
            location_description='vwgulrkemgypxsgedwso',
            probability='qitlkahkamitnhcgyctd',
            severity='rjhwpekmoyvhqyohlekm',
            management_type='drpuzrznwuwbnxjnorrg'
        )
        return instance

    
    def test_situation_record_id_property(self):
        """
        Test situation_record_id property
        """
        test_value = 'hcxzvnialkkixhpkqmue'
        self.instance.situation_record_id = test_value
        self.assertEqual(self.instance.situation_record_id, test_value)
    
    def test_version_time_property(self):
        """
        Test version_time property
        """
        test_value = 'wwetcximvzpqpiztaseo'
        self.instance.version_time = test_value
        self.assertEqual(self.instance.version_time, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'sdyueolcqkwvrlmpjivp'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'zwngshkdjmltkphsjlnf'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'mwocqsqhmuyxqoucrcmt'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'ojwhlgdfddqavenknwcy'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'fbhwfzbvuczfrqvtuezf'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'vwgulrkemgypxsgedwso'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_probability_property(self):
        """
        Test probability property
        """
        test_value = 'qitlkahkamitnhcgyctd'
        self.instance.probability = test_value
        self.assertEqual(self.instance.probability, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'rjhwpekmoyvhqyohlekm'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_management_type_property(self):
        """
        Test management_type property
        """
        test_value = 'drpuzrznwuwbnxjnorrg'
        self.instance.management_type = test_value
        self.assertEqual(self.instance.management_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Roadwork.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Roadwork.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

