"""
Test case for Unicast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.unicast import Unicast


class Test_Unicast(unittest.TestCase):
    """
    Test case for Unicast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Unicast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Unicast for testing
        """
        instance = Unicast(
            AddressStation1=int(43),
            Spare2=int(100),
            AddressStation2=int(40),
            Spare3=int(20)
        )
        return instance

    
    def test_AddressStation1_property(self):
        """
        Test AddressStation1 property
        """
        test_value = int(43)
        self.instance.AddressStation1 = test_value
        self.assertEqual(self.instance.AddressStation1, test_value)
    
    def test_Spare2_property(self):
        """
        Test Spare2 property
        """
        test_value = int(100)
        self.instance.Spare2 = test_value
        self.assertEqual(self.instance.Spare2, test_value)
    
    def test_AddressStation2_property(self):
        """
        Test AddressStation2 property
        """
        test_value = int(40)
        self.instance.AddressStation2 = test_value
        self.assertEqual(self.instance.AddressStation2, test_value)
    
    def test_Spare3_property(self):
        """
        Test Spare3 property
        """
        test_value = int(20)
        self.instance.Spare3 = test_value
        self.assertEqual(self.instance.Spare3, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Unicast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Unicast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

