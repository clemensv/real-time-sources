"""
Test case for CoordinatedUTCInquiry
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.coordinatedutcinquiry import CoordinatedUTCInquiry


class Test_CoordinatedUTCInquiry(unittest.TestCase):
    """
    Test case for CoordinatedUTCInquiry
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CoordinatedUTCInquiry.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CoordinatedUTCInquiry for testing
        """
        instance = CoordinatedUTCInquiry(
            MessageID=int(36),
            RepeatIndicator=int(68),
            UserID=int(99),
            Valid=False,
            Spare1=int(87),
            DestinationID=int(48),
            Spare2=int(47)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(36)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(68)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(99)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare1_property(self):
        """
        Test Spare1 property
        """
        test_value = int(87)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_DestinationID_property(self):
        """
        Test DestinationID property
        """
        test_value = int(48)
        self.instance.DestinationID = test_value
        self.assertEqual(self.instance.DestinationID, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(47)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CoordinatedUTCInquiry.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CoordinatedUTCInquiry.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

