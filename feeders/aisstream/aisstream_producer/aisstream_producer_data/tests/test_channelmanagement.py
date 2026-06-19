"""
Test case for ChannelManagement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.channelmanagement import ChannelManagement
from aisstream_producer_data.area import Area
from aisstream_producer_data.unicast import Unicast


class Test_ChannelManagement(unittest.TestCase):
    """
    Test case for ChannelManagement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ChannelManagement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ChannelManagement for testing
        """
        instance = ChannelManagement(
            MessageID=int(57),
            RepeatIndicator=int(72),
            UserID=int(91),
            Valid=True,
            Spare1=int(25),
            ChannelA=int(2),
            ChannelB=int(77),
            TxRxMode=int(28),
            LowPower=False,
            Area=None,
            Unicast=None,
            IsAddressed=True,
            BwA=True,
            BwB=True,
            TransitionalZoneSize=int(51),
            Spare4=int(13)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(57)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(72)
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
        test_value = int(25)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_ChannelA_property(self):
        """
        Test ChannelA property
        """
        test_value = int(2)
        self.instance.ChannelA = test_value
        self.assertEqual(self.instance.ChannelA, test_value)
    
    def test_ChannelB_property(self):
        """
        Test ChannelB property
        """
        test_value = int(77)
        self.instance.ChannelB = test_value
        self.assertEqual(self.instance.ChannelB, test_value)
    
    def test_TxRxMode_property(self):
        """
        Test TxRxMode property
        """
        test_value = int(28)
        self.instance.TxRxMode = test_value
        self.assertEqual(self.instance.TxRxMode, test_value)
    
    def test_LowPower_property(self):
        """
        Test LowPower property
        """
        test_value = False
        self.instance.LowPower = test_value
        self.assertEqual(self.instance.LowPower, test_value)
    
    def test_Area_property(self):
        """
        Test Area property
        """
        test_value = None
        self.instance.Area = test_value
        self.assertEqual(self.instance.Area, test_value)
    
    def test_Unicast_property(self):
        """
        Test Unicast property
        """
        test_value = None
        self.instance.Unicast = test_value
        self.assertEqual(self.instance.Unicast, test_value)
    
    def test_IsAddressed_property(self):
        """
        Test IsAddressed property
        """
        test_value = True
        self.instance.IsAddressed = test_value
        self.assertEqual(self.instance.IsAddressed, test_value)
    
    def test_BwA_property(self):
        """
        Test BwA property
        """
        test_value = True
        self.instance.BwA = test_value
        self.assertEqual(self.instance.BwA, test_value)
    
    def test_BwB_property(self):
        """
        Test BwB property
        """
        test_value = True
        self.instance.BwB = test_value
        self.assertEqual(self.instance.BwB, test_value)
    
    def test_TransitionalZoneSize_property(self):
        """
        Test TransitionalZoneSize property
        """
        test_value = int(51)
        self.instance.TransitionalZoneSize = test_value
        self.assertEqual(self.instance.TransitionalZoneSize, test_value)
    
    def test_Spare4_property(self):
        """
        Test Spare4 property
        """
        test_value = int(13)
        self.instance.Spare4 = test_value
        self.assertEqual(self.instance.Spare4, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ChannelManagement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ChannelManagement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

