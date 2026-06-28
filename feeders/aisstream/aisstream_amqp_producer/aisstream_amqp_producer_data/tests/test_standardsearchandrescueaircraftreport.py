"""
Test case for StandardSearchAndRescueAircraftReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.standardsearchandrescueaircraftreport import StandardSearchAndRescueAircraftReport


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
            MessageID=int(38),
            RepeatIndicator=int(63),
            UserID=int(72),
            Valid=True,
            Altitude=int(68),
            Sog=float(30.226247903650272),
            PositionAccuracy=False,
            Longitude=float(45.10238243529171),
            Latitude=float(65.7942339752232),
            Cog=float(25.332129162785467),
            Timestamp=int(69),
            AltFromBaro=True,
            Spare1=int(57),
            Dte=True,
            Spare2=int(81),
            AssignedMode=False,
            Raim=False,
            CommunicationStateIsItdma=False,
            CommunicationState=int(68)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(38)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(63)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(72)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Altitude_property(self):
        """
        Test Altitude property
        """
        test_value = int(68)
        self.instance.Altitude = test_value
        self.assertEqual(self.instance.Altitude, test_value)
    
    def test_Sog_property(self):
        """
        Test Sog property
        """
        test_value = float(30.226247903650272)
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
        test_value = float(45.10238243529171)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(65.7942339752232)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Cog_property(self):
        """
        Test Cog property
        """
        test_value = float(25.332129162785467)
        self.instance.Cog = test_value
        self.assertEqual(self.instance.Cog, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(69)
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
        test_value = int(57)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_Dte_property(self):
        """
        Test Dte property
        """
        test_value = True
        self.instance.Dte = test_value
        self.assertEqual(self.instance.Dte, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(81)
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
        test_value = False
        self.instance.CommunicationStateIsItdma = test_value
        self.assertEqual(self.instance.CommunicationStateIsItdma, test_value)
    
    def test_CommunicationState_property(self):
        """
        Test CommunicationState property
        """
        test_value = int(68)
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

