"""
Test case for PositionReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.positionreport import PositionReport


class Test_PositionReport(unittest.TestCase):
    """
    Test case for PositionReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PositionReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PositionReport for testing
        """
        instance = PositionReport(
            MessageID=int(56),
            RepeatIndicator=int(21),
            UserID=int(5),
            Valid=False,
            NavigationalStatus=int(33),
            RateOfTurn=int(85),
            Sog=float(80.23100963741201),
            PositionAccuracy=True,
            Longitude=float(69.68900496162846),
            Latitude=float(23.67668500804392),
            Cog=float(4.6410600127397394),
            TrueHeading=int(3),
            Timestamp=int(56),
            SpecialManoeuvreIndicator=int(87),
            Spare=int(58),
            Raim=True,
            CommunicationState=int(23)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(56)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(21)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(5)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_NavigationalStatus_property(self):
        """
        Test NavigationalStatus property
        """
        test_value = int(33)
        self.instance.NavigationalStatus = test_value
        self.assertEqual(self.instance.NavigationalStatus, test_value)
    
    def test_RateOfTurn_property(self):
        """
        Test RateOfTurn property
        """
        test_value = int(85)
        self.instance.RateOfTurn = test_value
        self.assertEqual(self.instance.RateOfTurn, test_value)
    
    def test_Sog_property(self):
        """
        Test Sog property
        """
        test_value = float(80.23100963741201)
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
        test_value = float(69.68900496162846)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(23.67668500804392)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Cog_property(self):
        """
        Test Cog property
        """
        test_value = float(4.6410600127397394)
        self.instance.Cog = test_value
        self.assertEqual(self.instance.Cog, test_value)
    
    def test_TrueHeading_property(self):
        """
        Test TrueHeading property
        """
        test_value = int(3)
        self.instance.TrueHeading = test_value
        self.assertEqual(self.instance.TrueHeading, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(56)
        self.instance.Timestamp = test_value
        self.assertEqual(self.instance.Timestamp, test_value)
    
    def test_SpecialManoeuvreIndicator_property(self):
        """
        Test SpecialManoeuvreIndicator property
        """
        test_value = int(87)
        self.instance.SpecialManoeuvreIndicator = test_value
        self.assertEqual(self.instance.SpecialManoeuvreIndicator, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(58)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Raim_property(self):
        """
        Test Raim property
        """
        test_value = True
        self.instance.Raim = test_value
        self.assertEqual(self.instance.Raim, test_value)
    
    def test_CommunicationState_property(self):
        """
        Test CommunicationState property
        """
        test_value = int(23)
        self.instance.CommunicationState = test_value
        self.assertEqual(self.instance.CommunicationState, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PositionReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PositionReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

