"""
Test case for StandardSearchAndRescueAircraftReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.standardsearchandrescueaircraftreport import StandardSearchAndRescueAircraftReport


class Test_StandardSearchAndRescueAircraftReport(unittest.TestCase):
    """
    Test case for StandardSearchAndRescueAircraftReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StandardSearchAndRescueAircraftReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StandardSearchAndRescueAircraftReport for testing
        """
        instance = StandardSearchAndRescueAircraftReport(
            MessageID=int(35),
            RepeatIndicator=int(11),
            UserID=int(75),
            Valid=False,
            Altitude=int(46),
            Sog=float(73.6158608572867),
            PositionAccuracy=True,
            Longitude=float(75.49484557113493),
            Latitude=float(61.58170240319072),
            Cog=float(60.840752761746465),
            Timestamp=int(49),
            AltFromBaro=True,
            Spare1=int(55),
            Dte=False,
            Spare2=int(68),
            AssignedMode=False,
            Raim=False,
            CommunicationStateIsItdma=True,
            CommunicationState=int(96)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(35)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(11)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(75)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Altitude_property(self):
        """
        Test Altitude property
        """
        test_value = int(46)
        self.instance.Altitude = test_value
        self.assertEqual(self.instance.Altitude, test_value)
    
    def test_Sog_property(self):
        """
        Test Sog property
        """
        test_value = float(73.6158608572867)
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
        test_value = float(75.49484557113493)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(61.58170240319072)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Cog_property(self):
        """
        Test Cog property
        """
        test_value = float(60.840752761746465)
        self.instance.Cog = test_value
        self.assertEqual(self.instance.Cog, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(49)
        self.instance.Timestamp = test_value
        self.assertEqual(self.instance.Timestamp, test_value)
    
    def test_AltFromBaro_property(self):
        """
        Test AltFromBaro property
        """
        test_value = True
        self.instance.AltFromBaro = test_value
        self.assertEqual(self.instance.AltFromBaro, test_value)
    
    def test_Spare1_property(self):
        """
        Test Spare1 property
        """
        test_value = int(55)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_Dte_property(self):
        """
        Test Dte property
        """
        test_value = False
        self.instance.Dte = test_value
        self.assertEqual(self.instance.Dte, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(68)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
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
        test_value = int(96)
        self.instance.CommunicationState = test_value
        self.assertEqual(self.instance.CommunicationState, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StandardSearchAndRescueAircraftReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StandardSearchAndRescueAircraftReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

