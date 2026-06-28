"""
Test case for Station2
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.station2 import Station2


class Test_Station2(unittest.TestCase):
    """
    Test case for Station2
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station2.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station2 for testing
        """
        instance = Station2(
            Valid=True,
            Spare1=int(62),
            StationID=int(48),
            MessageID=int(29),
            SlotOffset=int(20),
            Spare2=int(94)
        )
        return instance

    
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
        test_value = int(62)
        self.instance.Spare1 = test_value
        self.assertEqual(self.instance.Spare1, test_value)
    
    def test_StationID_property(self):
        """
        Test StationID property
        """
        test_value = int(48)
        self.instance.StationID = test_value
        self.assertEqual(self.instance.StationID, test_value)
    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(29)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_SlotOffset_property(self):
        """
        Test SlotOffset property
        """
        test_value = int(20)
        self.instance.SlotOffset = test_value
        self.assertEqual(self.instance.SlotOffset, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(94)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station2.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station2.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

