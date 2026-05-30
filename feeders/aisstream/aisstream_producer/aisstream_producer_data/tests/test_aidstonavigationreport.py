"""
Test case for AidsToNavigationReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.aidstonavigationreport import AidsToNavigationReport
from aisstream_producer_data.dimension import Dimension


class Test_AidsToNavigationReport(unittest.TestCase):
    """
    Test case for AidsToNavigationReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AidsToNavigationReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AidsToNavigationReport for testing
        """
        instance = AidsToNavigationReport(
            MessageID=int(51),
            RepeatIndicator=int(84),
            UserID=int(91),
            Valid=False,
            Type=int(15),
            Name='opkzytqfonsitmjbylcy',
            PositionAccuracy=False,
            Longitude=float(42.871218705469694),
            Latitude=float(17.995401783225528),
            Dimension=None,
            Fixtype=int(89),
            Timestamp=int(62),
            OffPosition=False,
            AtoN=int(36),
            Raim=False,
            VirtualAtoN=False,
            AssignedMode=True,
            Spare=False,
            NameExtension='vawqhqpoxhxjztkqvewd'
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(51)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(84)
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
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Type_property(self):
        """
        Test Type property
        """
        test_value = int(15)
        self.instance.Type = test_value
        self.assertEqual(self.instance.Type, test_value)
    
    def test_Name_property(self):
        """
        Test Name property
        """
        test_value = 'opkzytqfonsitmjbylcy'
        self.instance.Name = test_value
        self.assertEqual(self.instance.Name, test_value)
    
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
        test_value = float(42.871218705469694)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(17.995401783225528)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Dimension_property(self):
        """
        Test Dimension property
        """
        test_value = None
        self.instance.Dimension = test_value
        self.assertEqual(self.instance.Dimension, test_value)
    
    def test_Fixtype_property(self):
        """
        Test Fixtype property
        """
        test_value = int(89)
        self.instance.Fixtype = test_value
        self.assertEqual(self.instance.Fixtype, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(62)
        self.instance.Timestamp = test_value
        self.assertEqual(self.instance.Timestamp, test_value)
    
    def test_OffPosition_property(self):
        """
        Test OffPosition property
        """
        test_value = False
        self.instance.OffPosition = test_value
        self.assertEqual(self.instance.OffPosition, test_value)
    
    def test_AtoN_property(self):
        """
        Test AtoN property
        """
        test_value = int(36)
        self.instance.AtoN = test_value
        self.assertEqual(self.instance.AtoN, test_value)
    
    def test_Raim_property(self):
        """
        Test Raim property
        """
        test_value = False
        self.instance.Raim = test_value
        self.assertEqual(self.instance.Raim, test_value)
    
    def test_VirtualAtoN_property(self):
        """
        Test VirtualAtoN property
        """
        test_value = False
        self.instance.VirtualAtoN = test_value
        self.assertEqual(self.instance.VirtualAtoN, test_value)
    
    def test_AssignedMode_property(self):
        """
        Test AssignedMode property
        """
        test_value = True
        self.instance.AssignedMode = test_value
        self.assertEqual(self.instance.AssignedMode, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = False
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_NameExtension_property(self):
        """
        Test NameExtension property
        """
        test_value = 'vawqhqpoxhxjztkqvewd'
        self.instance.NameExtension = test_value
        self.assertEqual(self.instance.NameExtension, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AidsToNavigationReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AidsToNavigationReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

