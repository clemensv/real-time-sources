"""
Test case for BorderCrossing
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.border.bordercrossing import BorderCrossing


class Test_BorderCrossing(unittest.TestCase):
    """
    Test case for BorderCrossing
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BorderCrossing.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BorderCrossing for testing
        """
        instance = BorderCrossing(
            crossing_name='ufpzprhwysdcvnawqmop',
            wait_time=int(1),
            time='kicuhnxenjaatfvslalh',
            description='alczvzmjlqqffmtydmwj',
            road_name='kszzrkhlqpjydlhglykl',
            latitude=float(4.281464276555235),
            longitude=float(51.00188889873159)
        )
        return instance

    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'ufpzprhwysdcvnawqmop'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_wait_time_property(self):
        """
        Test wait_time property
        """
        test_value = int(1)
        self.instance.wait_time = test_value
        self.assertEqual(self.instance.wait_time, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'kicuhnxenjaatfvslalh'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'alczvzmjlqqffmtydmwj'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'kszzrkhlqpjydlhglykl'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(4.281464276555235)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(51.00188889873159)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BorderCrossing.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
