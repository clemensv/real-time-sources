"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rws_waterwebservices_producer_data.nl.rws.waterwebservices.station import Station


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
            code='tzrsmwlorucuxwbluyyk',
            name='opcgumzrhqggwimqmrui',
            latitude=float(6.353786692000951),
            longitude=float(46.50627138521709),
            coordinate_system='gbfrnejopbnsojsghjaf'
        )
        return instance

    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'tzrsmwlorucuxwbluyyk'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'opcgumzrhqggwimqmrui'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(6.353786692000951)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(46.50627138521709)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_coordinate_system_property(self):
        """
        Test coordinate_system property
        """
        test_value = 'gbfrnejopbnsojsghjaf'
        self.instance.coordinate_system = test_value
        self.assertEqual(self.instance.coordinate_system, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
