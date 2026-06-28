"""
Test case for ExtendedClassBPositionReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.extendedclassbpositionreport import ExtendedClassBPositionReport
from aisstream_amqp_producer_data.dimension import Dimension


class Test_ExtendedClassBPositionReport(unittest.TestCase):
    """
    Test case for ExtendedClassBPositionReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ExtendedClassBPositionReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ExtendedClassBPositionReport for testing
        """
        instance = ExtendedClassBPositionReport(
            MessageID=int(9),
            RepeatIndicator=int(96),
            UserID=int(35),
            Valid=True,
            Spare1=int(59),
            Sog=float(35.81521832035792),
            PositionAccuracy=False,
            Longitude=float(42.102949814264555),
            Latitude=float(31.119503300801732),
            Cog=float(31.870135194165663),
            TrueHeading=int(71),
            Timestamp=int(12),
            Spare2=int(79),
            Name='vvmrvgqmgemxftouehkt',
            Type=int(15),
            Dimension=None,
            FixType=int(50),
            Raim=True,
            Dte=False,
            AssignedMode=False,
            Spare3=int(61)
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(9)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(96)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(35)
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
        test_value = int(59)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_Sog_property(self):
        """
        Test Sog property
        """
        test_value = float(35.81521832035792)
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
        test_value = float(42.102949814264555)
        self.instance.Longitude = test_value
        self.assertEqual(self.instance.Longitude, test_value)
    
    def test_Latitude_property(self):
        """
        Test Latitude property
        """
        test_value = float(31.119503300801732)
        self.instance.Latitude = test_value
        self.assertEqual(self.instance.Latitude, test_value)
    
    def test_Cog_property(self):
        """
        Test Cog property
        """
        test_value = float(31.870135194165663)
        self.instance.Cog = test_value
        self.assertEqual(self.instance.Cog, test_value)
    
    def test_TrueHeading_property(self):
        """
        Test TrueHeading property
        """
        test_value = int(71)
        self.instance.TrueHeading = test_value
        self.assertEqual(self.instance.TrueHeading, test_value)
    
    def test_Timestamp_property(self):
        """
        Test Timestamp property
        """
        test_value = int(12)
        self.instance.Timestamp = test_value
        self.assertEqual(self.instance.Timestamp, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(79)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_Name_property(self):
        """
        Test Name property
        """
        test_value = 'vvmrvgqmgemxftouehkt'
        self.instance.Name = test_value
        self.assertEqual(self.instance.Name, test_value)
    
    def test_Type_property(self):
        """
        Test Type property
        """
        test_value = int(15)
        self.instance.Type = test_value
        self.assertEqual(self.instance.Type, test_value)
    
    def test_Dimension_property(self):
        """
        Test Dimension property
        """
        test_value = None
        self.instance.Dimension = test_value
        self.assertEqual(self.instance.Dimension, test_value)
    
    def test_FixType_property(self):
        """
        Test FixType property
        """
        test_value = int(50)
        self.instance.FixType = test_value
        self.assertEqual(self.instance.FixType, test_value)
    
    def test_Raim_property(self):
        """
        Test Raim property
        """
        test_value = True
        self.instance.Raim = test_value
        self.assertEqual(self.instance.Raim, test_value)
    
    def test_Dte_property(self):
        """
        Test Dte property
        """
        test_value = False
        self.instance.Dte = test_value
        self.assertEqual(self.instance.Dte, test_value)
    
    def test_AssignedMode_property(self):
        """
        Test AssignedMode property
        """
        test_value = False
        self.instance.AssignedMode = test_value
        self.assertEqual(self.instance.AssignedMode, test_value)
    
    def test_Spare3_property(self):
        """
        Test Spare3 property
        """
        test_value = int(61)
        self.instance.Spare3 = test_value
        self.assertEqual(self.instance.Spare3, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ExtendedClassBPositionReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ExtendedClassBPositionReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

