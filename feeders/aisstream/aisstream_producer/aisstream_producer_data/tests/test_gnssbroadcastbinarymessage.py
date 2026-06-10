"""
Test case for GnssBroadcastBinaryMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.gnssbroadcastbinarymessage import GnssBroadcastBinaryMessage


class Test_GnssBroadcastBinaryMessage(unittest.TestCase):
    """
    Test case for GnssBroadcastBinaryMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GnssBroadcastBinaryMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GnssBroadcastBinaryMessage for testing
        """
        instance = GnssBroadcastBinaryMessage(
            MessageID=int(21),
            RepeatIndicator=int(83),
            UserID=int(91),
            Valid=True,
            Spare1=int(70),
            Longitude=float(84.73887280968722),
            Latitude=float(34.64079341131943),
            Spare2=int(36),
            Data='jlszxczuashbqoakirqd'
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
        test_value = int(83)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(91)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare1_property(self):
        """
        Test Spare1 property
        """
        test_value = int(70)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_Longitude_property(self):
        """
        Test Longitude property
        """
        test_value = float(84.73887280968722)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(34.64079341131943)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(36)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_Data_property(self):
        """
        Test Data property
        """
        test_value = 'jlszxczuashbqoakirqd'
        self.instance.Data = test_value
        self.assertEqual(self.instance.Data, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GnssBroadcastBinaryMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GnssBroadcastBinaryMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

