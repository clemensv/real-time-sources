"""
Test case for Area
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.area import Area


class Test_Area(unittest.TestCase):
    """
    Test case for Area
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Area.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Area for testing
        """
        instance = Area(
            Longitude1=float(10.78836154963988),
            Latitude1=float(31.923362545214662),
            Longitude2=float(16.042037825289334),
            Latitude2=float(83.83601600149821)
        )
        return instance

    
    def test_Longitude1_property(self):
        """
        Test Longitude1 property
        """
        test_value = float(10.78836154963988)
        self.instance.Longitude1 = test_value
        self.assertEqual(self.instance.Longitude1, test_value)
    
    def test_Latitude1_property(self):
        """
        Test Latitude1 property
        """
        test_value = float(31.923362545214662)
        self.instance.Latitude1 = test_value
        self.assertEqual(self.instance.Latitude1, test_value)
    
    def test_Longitude2_property(self):
        """
        Test Longitude2 property
        """
        test_value = float(16.042037825289334)
        self.instance.Longitude2 = test_value
        self.assertEqual(self.instance.Longitude2, test_value)
    
    def test_Latitude2_property(self):
        """
        Test Latitude2 property
        """
        test_value = float(83.83601600149821)
        self.instance.Latitude2 = test_value
        self.assertEqual(self.instance.Latitude2, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Area.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Area.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

