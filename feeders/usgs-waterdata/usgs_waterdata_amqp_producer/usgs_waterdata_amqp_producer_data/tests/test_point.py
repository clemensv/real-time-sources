"""
Test case for Point
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_amqp_producer_data.usgs.waterdata.point import Point


class Test_Point(unittest.TestCase):
    """
    Test case for Point
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Point.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Point for testing
        """
        instance = Point(
            type='hozkntcrqjknuthwewso',
            coordinates=[float(56.185124185179724), float(48.228577292579104), float(33.23366118645603)]
        )
        return instance

    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'hozkntcrqjknuthwewso'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_coordinates_property(self):
        """
        Test coordinates property
        """
        test_value = [float(56.185124185179724), float(48.228577292579104), float(33.23366118645603)]
        self.instance.coordinates = test_value
        self.assertEqual(self.instance.coordinates, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Point.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Point.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

