"""
Test case for SafetyBroadcastMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.safetybroadcastmessage import SafetyBroadcastMessage


class Test_SafetyBroadcastMessage(unittest.TestCase):
    """
    Test case for SafetyBroadcastMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SafetyBroadcastMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SafetyBroadcastMessage for testing
        """
        instance = SafetyBroadcastMessage(
            MessageID=int(34),
            RepeatIndicator=int(87),
            UserID=int(55),
            Valid=True,
            Spare=int(54),
            Text='qsmbqulkofpozobdrdrp'
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(34)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(87)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(55)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(54)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Text_property(self):
        """
        Test Text property
        """
        test_value = 'qsmbqulkofpozobdrdrp'
        self.instance.Text = test_value
        self.assertEqual(self.instance.Text, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SafetyBroadcastMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SafetyBroadcastMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

