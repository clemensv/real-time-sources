"""
Test case for Document
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.aisstream_producer_data.document import Document


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
            MessageID=int(99),
            RepeatIndicator=int(70),
            UserID=int(91),
            Valid=True,
            UtcYear=int(39),
            UtcMonth=int(32),
            UtcDay=int(25),
            UtcHour=int(16),
            UtcMinute=int(79),
            UtcSecond=int(60),
            PositionAccuracy=True,
            Longitude=float(32.41184202613074),
            Latitude=float(38.51428518528203),
            FixType=int(1),
            LongRangeEnable=True,
            Spare=int(0),
            Raim=True,
            CommunicationState=int(40)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(99)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(70)
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
    
    def test_UtcYear_property(self):
        """
        Test UtcYear property
        """
        test_value = int(39)
        self.instance.UtcYear = test_value
        self.assertEqual(self.instance.UtcYear, test_value)
    
    def test_UtcMonth_property(self):
        """
        Test UtcMonth property
        """
        test_value = int(32)
        self.instance.UtcMonth = test_value
        self.assertEqual(self.instance.UtcMonth, test_value)
    
    def test_UtcDay_property(self):
        """
        Test UtcDay property
        """
        test_value = int(25)
        self.instance.UtcDay = test_value
        self.assertEqual(self.instance.UtcDay, test_value)
    
    def test_UtcHour_property(self):
        """
        Test UtcHour property
        """
        test_value = int(16)
        self.instance.UtcHour = test_value
        self.assertEqual(self.instance.UtcHour, test_value)
    
    def test_UtcMinute_property(self):
        """
        Test UtcMinute property
        """
        test_value = int(79)
        self.instance.UtcMinute = test_value
        self.assertEqual(self.instance.UtcMinute, test_value)
    
    def test_UtcSecond_property(self):
        """
        Test UtcSecond property
        """
        test_value = int(60)
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
        test_value = float(32.41184202613074)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(38.51428518528203)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_FixType_property(self):
        """
        Test FixType property
        """
        test_value = int(1)
        self.instance.FixType = test_value
        self.assertEqual(self.instance.FixType, test_value)
    
    def test_LongRangeEnable_property(self):
        """
        Test LongRangeEnable property
        """
        test_value = True
        self.instance.LongRangeEnable = test_value
        self.assertEqual(self.instance.LongRangeEnable, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(0)
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
        test_value = int(40)
        self.instance.CommunicationState = test_value
        self.assertEqual(self.instance.CommunicationState, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Document.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
