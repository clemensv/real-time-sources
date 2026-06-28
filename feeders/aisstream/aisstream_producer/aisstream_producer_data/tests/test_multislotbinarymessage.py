"""
Test case for MultiSlotBinaryMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.multislotbinarymessage import MultiSlotBinaryMessage
from aisstream_producer_data.applicationid import ApplicationID


class Test_MultiSlotBinaryMessage(unittest.TestCase):
    """
    Test case for MultiSlotBinaryMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MultiSlotBinaryMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MultiSlotBinaryMessage for testing
        """
        instance = MultiSlotBinaryMessage(
            MessageID=int(44),
            RepeatIndicator=int(89),
            UserID=int(42),
            Valid=False,
            DestinationIDValid=True,
            ApplicationIDValid=False,
            DestinationID=int(53),
            Spare1=int(37),
            ApplicationID=None,
            Payload='qqvnqltzchyxpsbgtqst',
            Spare2=int(71),
            CommunicationStateIsItdma=True,
            CommunicationState=int(55)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(44)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(89)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(42)
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
        test_value = True
        self.instance.DestinationIDValid = test_value
        self.assertEqual(self.instance.DestinationIDValid, test_value)
    
    def test_ApplicationIDValid_property(self):
        """
        Test ApplicationIDValid property
        """
        test_value = False
        self.instance.ApplicationIDValid = test_value
        self.assertEqual(self.instance.ApplicationIDValid, test_value)
    
    def test_DestinationID_property(self):
        """
        Test DestinationID property
        """
        test_value = int(53)
        self.instance.DestinationID = test_value
        self.assertEqual(self.instance.DestinationID, test_value)
    
    def test_Spare1_property(self):
        """
        Test Spare1 property
        """
        test_value = int(37)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
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
        test_value = 'qqvnqltzchyxpsbgtqst'
        self.instance.Payload = test_value
        self.assertEqual(self.instance.Payload, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(71)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_CommunicationStateIsItdma_property(self):
        """
        Test CommunicationStateIsItdma property
        """
        test_value = True
        self.instance.CommunicationStateIsItdma = test_value
        self.assertEqual(self.instance.CommunicationStateIsItdma, test_value)
    
    def test_CommunicationState_property(self):
        """
        Test CommunicationState property
        """
        test_value = int(55)
        self.instance.CommunicationState = test_value
        self.assertEqual(self.instance.CommunicationState, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MultiSlotBinaryMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MultiSlotBinaryMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

