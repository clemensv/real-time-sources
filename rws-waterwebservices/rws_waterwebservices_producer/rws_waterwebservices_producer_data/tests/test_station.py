"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rws_waterwebservices_producer_data.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            code='xvdccjrzlgnscghoqqhg',
            name='adcxekcjsjrsjaxnsynz',
            latitude=float(25.852582173320073),
            longitude=float(39.12273297455007),
            coordinate_system='ciyvcjbdnkjxofanaqry'
        )
        return instance

    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'xvdccjrzlgnscghoqqhg'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'adcxekcjsjrsjaxnsynz'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(25.852582173320073)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(39.12273297455007)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_coordinate_system_property(self):
        """
        Test coordinate_system property
        """
        test_value = 'ciyvcjbdnkjxofanaqry'
        self.instance.coordinate_system = test_value
        self.assertEqual(self.instance.coordinate_system, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

