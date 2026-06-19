"""
Test case for AddressedBinaryMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.addressedbinarymessage import AddressedBinaryMessage
from aisstream_producer_data.applicationid import ApplicationID


class Test_AddressedBinaryMessage(unittest.TestCase):
    """
    Test case for AddressedBinaryMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AddressedBinaryMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AddressedBinaryMessage for testing
        """
        instance = AddressedBinaryMessage(
            MessageID=int(97),
            RepeatIndicator=int(45),
            UserID=int(54),
            Valid=False,
            Sequenceinteger=int(92),
            DestinationID=int(63),
            Retransmission=True,
            Spare=True,
            ApplicationID=None,
            BinaryData='yjzglvjajviaugwvdaqt'
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(97)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(45)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(54)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Sequenceinteger_property(self):
        """
        Test Sequenceinteger property
        """
        test_value = int(92)
        self.instance.Sequenceinteger = test_value
        self.assertEqual(self.instance.Sequenceinteger, test_value)
    
    def test_DestinationID_property(self):
        """
        Test DestinationID property
        """
        test_value = int(63)
        self.instance.DestinationID = test_value
        self.assertEqual(self.instance.DestinationID, test_value)
    
    def test_Retransmission_property(self):
        """
        Test Retransmission property
        """
        test_value = True
        self.instance.Retransmission = test_value
        self.assertEqual(self.instance.Retransmission, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = True
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
        test_value = 'yjzglvjajviaugwvdaqt'
        self.instance.BinaryData = test_value
        self.assertEqual(self.instance.BinaryData, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AddressedBinaryMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AddressedBinaryMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

