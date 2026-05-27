"""
Test case for PortArea
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.portarea import PortArea


class Test_PortArea(unittest.TestCase):
    """
    Test case for PortArea
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PortArea.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PortArea for testing
        """
        instance = PortArea(
            port_area_code='kgswixxzbwraibvuqzdr',
            port_area_name='loyovkgvnrnkkniyrwft',
            longitude=float(0.4879849221234078),
            latitude=float(33.080346237373924)
        )
        return instance

    
    def test_port_area_code_property(self):
        """
        Test port_area_code property
        """
        test_value = 'kgswixxzbwraibvuqzdr'
        self.instance.port_area_code = test_value
        self.assertEqual(self.instance.port_area_code, test_value)
    
    def test_port_area_name_property(self):
        """
        Test port_area_name property
        """
        test_value = 'loyovkgvnrnkkniyrwft'
        self.instance.port_area_name = test_value
        self.assertEqual(self.instance.port_area_name, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(0.4879849221234078)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(33.080346237373924)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PortArea.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PortArea.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

