"""
Test case for StandardClassBPositionReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.standardclassbpositionreport import StandardClassBPositionReport


class Test_StandardClassBPositionReport(unittest.TestCase):
    """
    Test case for StandardClassBPositionReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StandardClassBPositionReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StandardClassBPositionReport for testing
        """
        instance = StandardClassBPositionReport(
            MessageID=int(5),
            RepeatIndicator=int(52),
            UserID=int(25),
            Valid=True,
            Spare1=int(3),
            Sog=float(84.14416971759289),
            PositionAccuracy=False,
            Longitude=float(9.592577572988759),
            Latitude=float(76.1824648544833),
            Cog=float(64.4231254314628),
            TrueHeading=int(87),
            Timestamp=int(94),
            Spare2=int(25),
            ClassBUnit=True,
            ClassBDisplay=True,
            ClassBDsc=False,
            ClassBBand=False,
            ClassBMsg22=False,
            AssignedMode=False,
            Raim=True,
            CommunicationStateIsItdma=False,
            CommunicationState=int(4)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(5)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(52)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(25)
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
        test_value = int(3)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_Sog_property(self):
        """
        Test Sog property
        """
        test_value = float(84.14416971759289)
        self.instance.Sog = test_value
        self.assertEqual(self.instance.Sog, test_value)
    
    def test_PositionAccuracy_property(self):
        """
        Test PositionAccuracy property
        """
        test_value = False
        self.instance.PositionAccuracy = test_value
        self.assertEqual(self.instance.PositionAccuracy, test_value)
    
    def test_Longitude_property(self):
        """
        Test Longitude property
        """
        test_value = float(9.592577572988759)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(76.1824648544833)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Cog_property(self):
        """
        Test Cog property
        """
        test_value = float(64.4231254314628)
        self.instance.Cog = test_value
        self.assertEqual(self.instance.Cog, test_value)
    
    def test_TrueHeading_property(self):
        """
        Test TrueHeading property
        """
        test_value = int(87)
        self.instance.TrueHeading = test_value
        self.assertEqual(self.instance.TrueHeading, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(94)
        self.instance.Timestamp = test_value
        self.assertEqual(self.instance.Timestamp, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(25)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_ClassBUnit_property(self):
        """
        Test ClassBUnit property
        """
        test_value = True
        self.instance.ClassBUnit = test_value
        self.assertEqual(self.instance.ClassBUnit, test_value)
    
    def test_ClassBDisplay_property(self):
        """
        Test ClassBDisplay property
        """
        test_value = True
        self.instance.ClassBDisplay = test_value
        self.assertEqual(self.instance.ClassBDisplay, test_value)
    
    def test_ClassBDsc_property(self):
        """
        Test ClassBDsc property
        """
        test_value = False
        self.instance.ClassBDsc = test_value
        self.assertEqual(self.instance.ClassBDsc, test_value)
    
    def test_ClassBBand_property(self):
        """
        Test ClassBBand property
        """
        test_value = False
        self.instance.ClassBBand = test_value
        self.assertEqual(self.instance.ClassBBand, test_value)
    
    def test_ClassBMsg22_property(self):
        """
        Test ClassBMsg22 property
        """
        test_value = False
        self.instance.ClassBMsg22 = test_value
        self.assertEqual(self.instance.ClassBMsg22, test_value)
    
    def test_AssignedMode_property(self):
        """
        Test AssignedMode property
        """
        test_value = False
        self.instance.AssignedMode = test_value
        self.assertEqual(self.instance.AssignedMode, test_value)
    
    def test_Raim_property(self):
        """
        Test Raim property
        """
        test_value = True
        self.instance.Raim = test_value
        self.assertEqual(self.instance.Raim, test_value)
    
    def test_CommunicationStateIsItdma_property(self):
        """
        Test CommunicationStateIsItdma property
        """
        test_value = False
        self.instance.CommunicationStateIsItdma = test_value
        self.assertEqual(self.instance.CommunicationStateIsItdma, test_value)
    
    def test_CommunicationState_property(self):
        """
        Test CommunicationState property
        """
        test_value = int(4)
        self.instance.CommunicationState = test_value
        self.assertEqual(self.instance.CommunicationState, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StandardClassBPositionReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StandardClassBPositionReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

