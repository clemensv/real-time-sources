"""
Test case for ReportB
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_mqtt_producer_data.reportb import ReportB
from aisstream_mqtt_producer_data.dimension import Dimension


class Test_ReportB(unittest.TestCase):
    """
    Test case for ReportB
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ReportB.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ReportB for testing
        """
        instance = ReportB(
            Valid=False,
            ShipType=int(20),
            VendorIDName='ksgdliiyhsokndmkgtsh',
            VenderIDModel=int(77),
            VenderIDSerial=int(79),
            CallSign='nquvoikijiyuhqqmnmau',
            Dimension=None,
            FixType=int(23),
            Spare=int(96)
        )
        return instance

    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_ShipType_property(self):
        """
        Test ShipType property
        """
        test_value = int(20)
        self.instance.ShipType = test_value
        self.assertEqual(self.instance.ShipType, test_value)
    
    def test_VendorIDName_property(self):
        """
        Test VendorIDName property
        """
        test_value = 'ksgdliiyhsokndmkgtsh'
        self.instance.VendorIDName = test_value
        self.assertEqual(self.instance.VendorIDName, test_value)
    
    def test_VenderIDModel_property(self):
        """
        Test VenderIDModel property
        """
        test_value = int(77)
        self.instance.VenderIDModel = test_value
        self.assertEqual(self.instance.VenderIDModel, test_value)
    
    def test_VenderIDSerial_property(self):
        """
        Test VenderIDSerial property
        """
        test_value = int(79)
        self.instance.VenderIDSerial = test_value
        self.assertEqual(self.instance.VenderIDSerial, test_value)
    
    def test_CallSign_property(self):
        """
        Test CallSign property
        """
        test_value = 'nquvoikijiyuhqqmnmau'
        self.instance.CallSign = test_value
        self.assertEqual(self.instance.CallSign, test_value)
    
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
        test_value = int(23)
        self.instance.FixType = test_value
        self.assertEqual(self.instance.FixType, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(96)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ReportB.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ReportB.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

