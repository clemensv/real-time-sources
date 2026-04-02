"""
Test case for Document
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.document import Document


class Test_Document(unittest.TestCase):
    """
    Test case for Document
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Document.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Document for testing
        """
        instance = Document(
            MessageID=int(98),
            RepeatIndicator=int(61),
            UserID=int(57),
            Valid=False,
            Spare1=int(0),
            Sog=float(75.33574414333576),
            PositionAccuracy=True,
            Longitude=float(72.44817311345284),
            Latitude=float(27.793638048277437),
            Cog=float(54.59374257727968),
            TrueHeading=int(49),
            Timestamp=int(79),
            Spare2=int(36),
            ClassBUnit=False,
            ClassBDisplay=True,
            ClassBDsc=False,
            ClassBBand=False,
            ClassBMsg22=True,
            AssignedMode=False,
            Raim=False,
            CommunicationStateIsItdma=True,
            CommunicationState=int(93)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(98)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(61)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(57)
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
        test_value = int(0)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_Sog_property(self):
        """
        Test Sog property
        """
        test_value = float(75.33574414333576)
        self.instance.Sog = test_value
        self.assertEqual(self.instance.Sog, test_value)
    
    def test_PositionAccuracy_property(self):
        """
        Test PositionAccuracy property
        """
        test_value = True
        self.instance.PositionAccuracy = test_value
        self.assertEqual(self.instance.PositionAccuracy, test_value)
    
    def test_Longitude_property(self):
        """
        Test Longitude property
        """
        test_value = float(72.44817311345284)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(27.793638048277437)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Cog_property(self):
        """
        Test Cog property
        """
        test_value = float(54.59374257727968)
        self.instance.Cog = test_value
        self.assertEqual(self.instance.Cog, test_value)
    
    def test_TrueHeading_property(self):
        """
        Test TrueHeading property
        """
        test_value = int(49)
        self.instance.TrueHeading = test_value
        self.assertEqual(self.instance.TrueHeading, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(79)
        self.instance.Timestamp = test_value
        self.assertEqual(self.instance.Timestamp, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(36)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_ClassBUnit_property(self):
        """
        Test ClassBUnit property
        """
        test_value = False
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
        test_value = True
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
        test_value = False
        self.instance.Raim = test_value
        self.assertEqual(self.instance.Raim, test_value)
    
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
        test_value = int(93)
        self.instance.CommunicationState = test_value
        self.assertEqual(self.instance.CommunicationState, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Document.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Document.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

