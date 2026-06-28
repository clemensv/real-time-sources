"""
Test case for BinaryAcknowledge
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_mqtt_producer_data.binaryacknowledge import BinaryAcknowledge


class Test_BinaryAcknowledge(unittest.TestCase):
    """
    Test case for BinaryAcknowledge
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BinaryAcknowledge.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BinaryAcknowledge for testing
        """
        instance = BinaryAcknowledge(
            MessageID=int(38),
            RepeatIndicator=int(83),
            UserID=int(93),
            Valid=False,
            Spare=int(97),
            Destinations={'kpsuuctilqsfefnowoga': 'lmyqhmhnkeiqgotqncuk', 'vsyyyslcpuacvmworsla': 'uqaxlhccdckoxcyjewft', 'ivcektjvwjcqzgyqigfq': 'nogwacellychwprtbivu'}
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(38)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(83)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(93)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(97)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Destinations_property(self):
        """
        Test Destinations property
        """
        test_value = {'kpsuuctilqsfefnowoga': 'lmyqhmhnkeiqgotqncuk', 'vsyyyslcpuacvmworsla': 'uqaxlhccdckoxcyjewft', 'ivcektjvwjcqzgyqigfq': 'nogwacellychwprtbivu'}
        self.instance.Destinations = test_value
        self.assertEqual(self.instance.Destinations, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BinaryAcknowledge.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BinaryAcknowledge.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

