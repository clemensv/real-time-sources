"""
Test case for SafetyRelatedMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_amqp_producer_data.safetyrelatedmessage import SafetyRelatedMessage


class Test_SafetyRelatedMessage(unittest.TestCase):
    """
    Test case for SafetyRelatedMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SafetyRelatedMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SafetyRelatedMessage for testing
        """
        instance = SafetyRelatedMessage(
            situation_record_id='ldupwbvpohcrjaqffnng',
            version_time='zpzgbyozdmvsdsgryxqj',
            validity_status='snmbxpvikafojidujowt',
            start_time='lojzidexhejvuaymmsdh',
            end_time='zghtzddbfgvtpfytxhmu',
            road_name='uagqoemqebjbjlbkfsww',
            message_type='saxjtestncaojsiuwpzu',
            description='wkrvkfjikjkmjsygmqdj',
            urgency='bnuxbpiazjciqrccewxh'
        )
        return instance

    
    def test_situation_record_id_property(self):
        """
        Test situation_record_id property
        """
        test_value = 'ldupwbvpohcrjaqffnng'
        self.instance.situation_record_id = test_value
        self.assertEqual(self.instance.situation_record_id, test_value)
    
    def test_version_time_property(self):
        """
        Test version_time property
        """
        test_value = 'zpzgbyozdmvsdsgryxqj'
        self.instance.version_time = test_value
        self.assertEqual(self.instance.version_time, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'snmbxpvikafojidujowt'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'lojzidexhejvuaymmsdh'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'zghtzddbfgvtpfytxhmu'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'uagqoemqebjbjlbkfsww'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_message_type_property(self):
        """
        Test message_type property
        """
        test_value = 'saxjtestncaojsiuwpzu'
        self.instance.message_type = test_value
        self.assertEqual(self.instance.message_type, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'wkrvkfjikjkmjsygmqdj'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = 'bnuxbpiazjciqrccewxh'
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SafetyRelatedMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SafetyRelatedMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

