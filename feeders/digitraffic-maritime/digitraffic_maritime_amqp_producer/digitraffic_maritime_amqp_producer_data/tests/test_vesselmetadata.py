"""
Test case for VesselMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_amqp_producer_data.vesselmetadata import VesselMetadata


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
            mmsi=int(75),
            timestamp=int(47),
            name='ujqdfouwjjmhzguiqtgh',
            callSign='wpctdoyzsicrbvctcmwu',
            imo=int(90),
            type=int(54),
            draught=int(10),
            eta=int(52),
            destination='wfhuxrraehifbnzsxpjn',
            posType=int(32),
            refA=int(72),
            refB=int(14),
            refC=int(50),
            refD=int(99)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(75)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(47)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ujqdfouwjjmhzguiqtgh'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_callSign_property(self):
        """
        Test callSign property
        """
        test_value = 'wpctdoyzsicrbvctcmwu'
        self.instance.callSign = test_value
        self.assertEqual(self.instance.callSign, test_value)
    
    def test_imo_property(self):
        """
        Test imo property
        """
        test_value = int(90)
        self.instance.imo = test_value
        self.assertEqual(self.instance.imo, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = int(54)
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = int(10)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = int(52)
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'wfhuxrraehifbnzsxpjn'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_posType_property(self):
        """
        Test posType property
        """
        test_value = int(32)
        self.instance.posType = test_value
        self.assertEqual(self.instance.posType, test_value)
    
    def test_refA_property(self):
        """
        Test refA property
        """
        test_value = int(72)
        self.instance.refA = test_value
        self.assertEqual(self.instance.refA, test_value)
    
    def test_refB_property(self):
        """
        Test refB property
        """
        test_value = int(14)
        self.instance.refB = test_value
        self.assertEqual(self.instance.refB, test_value)
    
    def test_refC_property(self):
        """
        Test refC property
        """
        test_value = int(50)
        self.instance.refC = test_value
        self.assertEqual(self.instance.refC, test_value)
    
    def test_refD_property(self):
        """
        Test refD property
        """
        test_value = int(99)
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

