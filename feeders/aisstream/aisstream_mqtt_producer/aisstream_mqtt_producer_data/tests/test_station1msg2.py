"""
Test case for Station1Msg2
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_mqtt_producer_data.station1msg2 import Station1Msg2


class Test_Station1Msg2(unittest.TestCase):
    """
    Test case for Station1Msg2
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station1Msg2.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station1Msg2 for testing
        """
        instance = Station1Msg2(
            Valid=True,
            Spare=int(35),
            MessageID=int(57),
            SlotOffset=int(18)
        )
        return instance

    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(35)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(57)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_SlotOffset_property(self):
        """
        Test SlotOffset property
        """
        test_value = int(18)
        self.instance.SlotOffset = test_value
        self.assertEqual(self.instance.SlotOffset, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station1Msg2.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station1Msg2.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

