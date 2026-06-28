"""
Test case for BaseStationReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.basestationreport import BaseStationReport


class Test_BaseStationReport(unittest.TestCase):
    """
    Test case for BaseStationReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BaseStationReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BaseStationReport for testing
        """
        instance = BaseStationReport(
            MessageID=int(20),
            RepeatIndicator=int(32),
            UserID=int(72),
            Valid=True,
            UtcYear=int(26),
            UtcMonth=int(28),
            UtcDay=int(15),
            UtcHour=int(52),
            UtcMinute=int(47),
            UtcSecond=int(6),
            PositionAccuracy=True,
            Longitude=float(17.880470199230647),
            Latitude=float(1.7471055701011151),
            FixType=int(46),
            LongRangeEnable=False,
            Spare=int(95),
            Raim=False,
            CommunicationState=int(47)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(20)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(32)
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
    
    def test_UtcYear_property(self):
        """
        Test UtcYear property
        """
        test_value = int(26)
        self.instance.UtcYear = test_value
        self.assertEqual(self.instance.UtcYear, test_value)
    
    def test_UtcMonth_property(self):
        """
        Test UtcMonth property
        """
        test_value = int(28)
        self.instance.UtcMonth = test_value
        self.assertEqual(self.instance.UtcMonth, test_value)
    
    def test_UtcDay_property(self):
        """
        Test UtcDay property
        """
        test_value = int(15)
        self.instance.UtcDay = test_value
        self.assertEqual(self.instance.UtcDay, test_value)
    
    def test_UtcHour_property(self):
        """
        Test UtcHour property
        """
        test_value = int(52)
        self.instance.UtcHour = test_value
        self.assertEqual(self.instance.UtcHour, test_value)
    
    def test_UtcMinute_property(self):
        """
        Test UtcMinute property
        """
        test_value = int(47)
        self.instance.UtcMinute = test_value
        self.assertEqual(self.instance.UtcMinute, test_value)
    
    def test_UtcSecond_property(self):
        """
        Test UtcSecond property
        """
        test_value = int(6)
        self.instance.UtcSecond = test_value
        self.assertEqual(self.instance.UtcSecond, test_value)
    
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
        test_value = float(17.880470199230647)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(1.7471055701011151)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_FixType_property(self):
        """
        Test FixType property
        """
        test_value = int(46)
        self.instance.FixType = test_value
        self.assertEqual(self.instance.FixType, test_value)
    
    def test_LongRangeEnable_property(self):
        """
        Test LongRangeEnable property
        """
        test_value = False
        self.instance.LongRangeEnable = test_value
        self.assertEqual(self.instance.LongRangeEnable, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(95)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Raim_property(self):
        """
        Test Raim property
        """
        test_value = False
        self.instance.Raim = test_value
        self.assertEqual(self.instance.Raim, test_value)
    
    def test_CommunicationState_property(self):
        """
        Test CommunicationState property
        """
        test_value = int(47)
        self.instance.CommunicationState = test_value
        self.assertEqual(self.instance.CommunicationState, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BaseStationReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BaseStationReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

