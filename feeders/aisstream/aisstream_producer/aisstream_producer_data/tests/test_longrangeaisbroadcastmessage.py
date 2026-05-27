"""
Test case for LongRangeAisBroadcastMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.longrangeaisbroadcastmessage import LongRangeAisBroadcastMessage


class Test_LongRangeAisBroadcastMessage(unittest.TestCase):
    """
    Test case for LongRangeAisBroadcastMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LongRangeAisBroadcastMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LongRangeAisBroadcastMessage for testing
        """
        instance = LongRangeAisBroadcastMessage(
            MessageID=int(94),
            RepeatIndicator=int(96),
            UserID=int(3),
            Valid=True,
            PositionAccuracy=False,
            Raim=True,
            NavigationalStatus=int(13),
            Longitude=float(4.590061848369887),
            Latitude=float(14.810029386007573),
            Sog=float(25.82777492783349),
            Cog=float(2.0241213890948795),
            PositionLatency=True,
            Spare=False
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(94)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(96)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(3)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_PositionAccuracy_property(self):
        """
        Test PositionAccuracy property
        """
        test_value = False
        self.instance.PositionAccuracy = test_value
        self.assertEqual(self.instance.PositionAccuracy, test_value)
    
    def test_Raim_property(self):
        """
        Test Raim property
        """
        test_value = True
        self.instance.Raim = test_value
        self.assertEqual(self.instance.Raim, test_value)
    
    def test_NavigationalStatus_property(self):
        """
        Test NavigationalStatus property
        """
        test_value = int(13)
        self.instance.NavigationalStatus = test_value
        self.assertEqual(self.instance.NavigationalStatus, test_value)
    
    def test_Longitude_property(self):
        """
        Test Longitude property
        """
        test_value = float(4.590061848369887)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(14.810029386007573)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Sog_property(self):
        """
        Test Sog property
        """
        test_value = float(25.82777492783349)
        self.instance.Sog = test_value
        self.assertEqual(self.instance.Sog, test_value)
    
    def test_Cog_property(self):
        """
        Test Cog property
        """
        test_value = float(2.0241213890948795)
        self.instance.Cog = test_value
        self.assertEqual(self.instance.Cog, test_value)
    
    def test_PositionLatency_property(self):
        """
        Test PositionLatency property
        """
        test_value = True
        self.instance.PositionLatency = test_value
        self.assertEqual(self.instance.PositionLatency, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = False
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LongRangeAisBroadcastMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LongRangeAisBroadcastMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

