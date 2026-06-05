"""
Test case for VesselMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.vesselmetadata import VesselMetadata


class Test_VesselMetadata(unittest.TestCase):
    """
    Test case for VesselMetadata
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselMetadata.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselMetadata for testing
        """
        instance = VesselMetadata(
            mmsi=int(90),
            timestamp=int(43),
            name='jqfjfpubivwpanfdtxau',
            callSign='lczezjgwawmtkqekfamx',
            imo=int(41),
            type=int(91),
            draught=int(40),
            eta=int(90),
            destination='inlokvzfkghvohjijten',
            posType=int(98),
            refA=int(68),
            refB=int(56),
            refC=int(99),
            refD=int(42)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(90)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(43)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'jqfjfpubivwpanfdtxau'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_callSign_property(self):
        """
        Test callSign property
        """
        test_value = 'lczezjgwawmtkqekfamx'
        self.instance.callSign = test_value
        self.assertEqual(self.instance.callSign, test_value)
    
    def test_imo_property(self):
        """
        Test imo property
        """
        test_value = int(41)
        self.instance.imo = test_value
        self.assertEqual(self.instance.imo, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = int(91)
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = int(40)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = int(90)
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'inlokvzfkghvohjijten'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_posType_property(self):
        """
        Test posType property
        """
        test_value = int(98)
        self.instance.posType = test_value
        self.assertEqual(self.instance.posType, test_value)
    
    def test_refA_property(self):
        """
        Test refA property
        """
        test_value = int(68)
        self.instance.refA = test_value
        self.assertEqual(self.instance.refA, test_value)
    
    def test_refB_property(self):
        """
        Test refB property
        """
        test_value = int(56)
        self.instance.refB = test_value
        self.assertEqual(self.instance.refB, test_value)
    
    def test_refC_property(self):
        """
        Test refC property
        """
        test_value = int(99)
        self.instance.refC = test_value
        self.assertEqual(self.instance.refC, test_value)
    
    def test_refD_property(self):
        """
        Test refD property
        """
        test_value = int(42)
        self.instance.refD = test_value
        self.assertEqual(self.instance.refD, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselMetadata.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselMetadata.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

