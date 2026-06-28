"""
Test case for SingleSlotBinaryMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.singleslotbinarymessage import SingleSlotBinaryMessage
from aisstream_producer_data.applicationid import ApplicationID


class Test_SingleSlotBinaryMessage(unittest.TestCase):
    """
    Test case for SingleSlotBinaryMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SingleSlotBinaryMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SingleSlotBinaryMessage for testing
        """
        instance = SingleSlotBinaryMessage(
            MessageID=int(20),
            RepeatIndicator=int(80),
            UserID=int(67),
            Valid=False,
            DestinationIDValid=False,
            ApplicationIDValid=True,
            DestinationID=int(95),
            Spare=int(25),
            ApplicationID=None,
            Payload='mgwgblfttyifvzstdvss'
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(20)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(80)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(67)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_DestinationIDValid_property(self):
        """
        Test DestinationIDValid property
        """
        test_value = False
        self.instance.DestinationIDValid = test_value
        self.assertEqual(self.instance.DestinationIDValid, test_value)
    
    def test_ApplicationIDValid_property(self):
        """
        Test ApplicationIDValid property
        """
        test_value = True
        self.instance.ApplicationIDValid = test_value
        self.assertEqual(self.instance.ApplicationIDValid, test_value)
    
    def test_DestinationID_property(self):
        """
        Test DestinationID property
        """
        test_value = int(95)
        self.instance.DestinationID = test_value
        self.assertEqual(self.instance.DestinationID, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(25)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_ApplicationID_property(self):
        """
        Test ApplicationID property
        """
        test_value = None
        self.instance.ApplicationID = test_value
        self.assertEqual(self.instance.ApplicationID, test_value)
    
    def test_Payload_property(self):
        """
        Test Payload property
        """
        test_value = 'mgwgblfttyifvzstdvss'
        self.instance.Payload = test_value
        self.assertEqual(self.instance.Payload, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SingleSlotBinaryMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SingleSlotBinaryMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

