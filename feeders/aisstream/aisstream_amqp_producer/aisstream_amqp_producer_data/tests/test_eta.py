"""
Test case for Eta
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.eta import Eta


class Test_Eta(unittest.TestCase):
    """
    Test case for Eta
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Eta.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Eta for testing
        """
        instance = Eta(
            Month=int(1),
            Day=int(18),
            Hour=int(42),
            Minute=int(47)
        )
        return instance

    
    def test_Month_property(self):
        """
        Test Month property
        """
        test_value = int(1)
        self.instance.Month = test_value
        self.assertEqual(self.instance.Month, test_value)
    
    def test_Day_property(self):
        """
        Test Day property
        """
        test_value = int(18)
        self.instance.Day = test_value
        self.assertEqual(self.instance.Day, test_value)
    
    def test_Hour_property(self):
        """
        Test Hour property
        """
        test_value = int(42)
        self.instance.Hour = test_value
        self.assertEqual(self.instance.Hour, test_value)
    
    def test_Minute_property(self):
        """
        Test Minute property
        """
        test_value = int(47)
        self.instance.Minute = test_value
        self.assertEqual(self.instance.Minute, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Eta.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Eta.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

