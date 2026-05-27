"""
Test case for AddressedSafetyMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.addressedsafetymessage import AddressedSafetyMessage


class Test_AddressedSafetyMessage(unittest.TestCase):
    """
    Test case for AddressedSafetyMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AddressedSafetyMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AddressedSafetyMessage for testing
        """
        instance = AddressedSafetyMessage(
            MessageID=int(21),
            RepeatIndicator=int(63),
            UserID=int(26),
            Valid=False,
            Sequenceinteger=int(92),
            DestinationID=int(58),
            Retransmission=True,
            Spare=True,
            Text='cstmlisuploggjwiobat'
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(21)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(63)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(26)
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
        test_value = int(58)
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
    
    def test_Text_property(self):
        """
        Test Text property
        """
        test_value = 'cstmlisuploggjwiobat'
        self.instance.Text = test_value
        self.assertEqual(self.instance.Text, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AddressedSafetyMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AddressedSafetyMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

