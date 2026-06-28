"""
Test case for ShipStaticData
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.shipstaticdata import ShipStaticData
from aisstream_producer_data.eta import Eta
from aisstream_producer_data.dimension import Dimension


class Test_ShipStaticData(unittest.TestCase):
    """
    Test case for ShipStaticData
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ShipStaticData.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ShipStaticData for testing
        """
        instance = ShipStaticData(
            MessageID=int(3),
            RepeatIndicator=int(16),
            UserID=int(20),
            Valid=True,
            AisVersion=int(100),
            ImoNumber=int(42),
            CallSign='dzeorggqerqsrkvlslty',
            Name='eztpktewzvphqzapzbui',
            Type=int(91),
            Dimension=None,
            FixType=int(10),
            Eta=None,
            MaximumStaticDraught=float(38.91275748166642),
            Destination='wrhzsvzuyzzjlwkvkgjk',
            Dte=False,
            Spare=True
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(3)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(16)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(20)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_AisVersion_property(self):
        """
        Test AisVersion property
        """
        test_value = int(100)
        self.instance.AisVersion = test_value
        self.assertEqual(self.instance.AisVersion, test_value)
    
    def test_ImoNumber_property(self):
        """
        Test ImoNumber property
        """
        test_value = int(42)
        self.instance.ImoNumber = test_value
        self.assertEqual(self.instance.ImoNumber, test_value)
    
    def test_CallSign_property(self):
        """
        Test CallSign property
        """
        test_value = 'dzeorggqerqsrkvlslty'
        self.instance.CallSign = test_value
        self.assertEqual(self.instance.CallSign, test_value)
    
    def test_Name_property(self):
        """
        Test Name property
        """
        test_value = 'eztpktewzvphqzapzbui'
        self.instance.Name = test_value
        self.assertEqual(self.instance.Name, test_value)
    
    def test_Type_property(self):
        """
        Test Type property
        """
        test_value = int(91)
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
        test_value = int(10)
        self.instance.FixType = test_value
        self.assertEqual(self.instance.FixType, test_value)
    
    def test_Eta_property(self):
        """
        Test Eta property
        """
        test_value = None
        self.instance.Eta = test_value
        self.assertEqual(self.instance.Eta, test_value)
    
    def test_MaximumStaticDraught_property(self):
        """
        Test MaximumStaticDraught property
        """
        test_value = float(38.91275748166642)
        self.instance.MaximumStaticDraught = test_value
        self.assertEqual(self.instance.MaximumStaticDraught, test_value)
    
    def test_Destination_property(self):
        """
        Test Destination property
        """
        test_value = 'wrhzsvzuyzzjlwkvkgjk'
        self.instance.Destination = test_value
        self.assertEqual(self.instance.Destination, test_value)
    
    def test_Dte_property(self):
        """
        Test Dte property
        """
        test_value = False
        self.instance.Dte = test_value
        self.assertEqual(self.instance.Dte, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = True
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ShipStaticData.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ShipStaticData.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

