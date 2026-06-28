"""
Test case for BinaryBroadcastMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.binarybroadcastmessage import BinaryBroadcastMessage
from aisstream_producer_data.applicationid import ApplicationID


class Test_BinaryBroadcastMessage(unittest.TestCase):
    """
    Test case for BinaryBroadcastMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BinaryBroadcastMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BinaryBroadcastMessage for testing
        """
        instance = BinaryBroadcastMessage(
            MessageID=int(19),
            RepeatIndicator=int(10),
            UserID=int(64),
            Valid=False,
            Spare=int(30),
            ApplicationID=None,
            BinaryData='lwsmmwdtcqzjwxnaanyy'
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(19)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(10)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(64)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(30)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_ApplicationID_property(self):
        """
        Test ApplicationID property
        """
        test_value = None
        self.instance.ApplicationID = test_value
        self.assertEqual(self.instance.ApplicationID, test_value)
    
    def test_BinaryData_property(self):
        """
        Test BinaryData property
        """
        test_value = 'lwsmmwdtcqzjwxnaanyy'
        self.instance.BinaryData = test_value
        self.assertEqual(self.instance.BinaryData, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BinaryBroadcastMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BinaryBroadcastMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

