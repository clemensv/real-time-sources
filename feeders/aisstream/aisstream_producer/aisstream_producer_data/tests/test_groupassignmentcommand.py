"""
Test case for GroupAssignmentCommand
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.groupassignmentcommand import GroupAssignmentCommand


class Test_GroupAssignmentCommand(unittest.TestCase):
    """
    Test case for GroupAssignmentCommand
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GroupAssignmentCommand.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GroupAssignmentCommand for testing
        """
        instance = GroupAssignmentCommand(
            MessageID=int(39),
            RepeatIndicator=int(30),
            UserID=int(66),
            Valid=False,
            Spare1=int(9),
            Longitude1=float(74.99130332236062),
            Latitude1=float(93.11185140561375),
            Longitude2=float(51.95708813738852),
            Latitude2=float(33.649938435759054),
            StationType=int(20),
            ShipType=int(50),
            Spare2=int(33),
            TxRxMode=int(29),
            ReportingInterval=int(66),
            QuietTime=int(69),
            Spare3=int(81)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(39)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(30)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(66)
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
        test_value = int(9)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_Longitude1_property(self):
        """
        Test Longitude1 property
        """
        test_value = float(74.99130332236062)
        self.instance.Longitude1 = test_value
        self.assertEqual(self.instance.Longitude1, test_value)
    
    def test_Latitude1_property(self):
        """
        Test Latitude1 property
        """
        test_value = float(93.11185140561375)
        self.instance.Latitude1 = test_value
        self.assertEqual(self.instance.Latitude1, test_value)
    
    def test_Longitude2_property(self):
        """
        Test Longitude2 property
        """
        test_value = float(51.95708813738852)
        self.instance.Longitude2 = test_value
        self.assertEqual(self.instance.Longitude2, test_value)
    
    def test_Latitude2_property(self):
        """
        Test Latitude2 property
        """
        test_value = float(33.649938435759054)
        self.instance.Latitude2 = test_value
        self.assertEqual(self.instance.Latitude2, test_value)
    
    def test_StationType_property(self):
        """
        Test StationType property
        """
        test_value = int(20)
        self.instance.StationType = test_value
        self.assertEqual(self.instance.StationType, test_value)
    
    def test_ShipType_property(self):
        """
        Test ShipType property
        """
        test_value = int(50)
        self.instance.ShipType = test_value
        self.assertEqual(self.instance.ShipType, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(33)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_TxRxMode_property(self):
        """
        Test TxRxMode property
        """
        test_value = int(29)
        self.instance.TxRxMode = test_value
        self.assertEqual(self.instance.TxRxMode, test_value)
    
    def test_ReportingInterval_property(self):
        """
        Test ReportingInterval property
        """
        test_value = int(66)
        self.instance.ReportingInterval = test_value
        self.assertEqual(self.instance.ReportingInterval, test_value)
    
    def test_QuietTime_property(self):
        """
        Test QuietTime property
        """
        test_value = int(69)
        self.instance.QuietTime = test_value
        self.assertEqual(self.instance.QuietTime, test_value)
    
    def test_Spare3_property(self):
        """
        Test Spare3 property
        """
        test_value = int(81)
        self.instance.Spare3 = test_value
        self.assertEqual(self.instance.Spare3, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GroupAssignmentCommand.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GroupAssignmentCommand.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

