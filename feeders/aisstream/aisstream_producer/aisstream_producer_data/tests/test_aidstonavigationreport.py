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
            MessageID=int(98),
            RepeatIndicator=int(38),
            UserID=int(51),
            Valid=False,
            Type=int(94),
            Name='szhpydlhfwdrlweyvsth',
            PositionAccuracy=True,
            Longitude=float(74.77101768550622),
            Latitude=float(46.24778415017523),
            Dimension=None,
            Fixtype=int(23),
            Timestamp=int(39),
            OffPosition=True,
            AtoN=int(10),
            Raim=True,
            VirtualAtoN=False,
            AssignedMode=False,
            Spare=True,
            NameExtension='izegwvjjrsybhqqagfnb'
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
        test_value = int(38)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(51)
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
        test_value = int(94)
        self.instance.Type = test_value
        self.assertEqual(self.instance.Type, test_value)
    
    def test_Name_property(self):
        """
        Test Name property
        """
        test_value = 'szhpydlhfwdrlweyvsth'
        self.instance.Name = test_value
        self.assertEqual(self.instance.Name, test_value)
    
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
        test_value = float(74.77101768550622)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(46.24778415017523)
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
        test_value = int(23)
        self.instance.Fixtype = test_value
        self.assertEqual(self.instance.Fixtype, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(39)
        self.instance.Timestamp = test_value
        self.assertEqual(self.instance.Timestamp, test_value)
    
    def test_OffPosition_property(self):
        """
        Test OffPosition property
        """
        test_value = True
        self.instance.OffPosition = test_value
        self.assertEqual(self.instance.OffPosition, test_value)
    
    def test_AtoN_property(self):
        """
        Test AtoN property
        """
        test_value = int(10)
        self.instance.AtoN = test_value
        self.assertEqual(self.instance.AtoN, test_value)
    
    def test_Raim_property(self):
        """
        Test Raim property
        """
        test_value = True
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
        test_value = False
        self.instance.AssignedMode = test_value
        self.assertEqual(self.instance.AssignedMode, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = True
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_NameExtension_property(self):
        """
        Test NameExtension property
        """
        test_value = 'izegwvjjrsybhqqagfnb'
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

