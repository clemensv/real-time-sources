"""
Test case for UnnamedClass
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_amqp_producer_data.microsoft.opendata.us.noaa.unnamedclass import UnnamedClass


class Test_UnnamedClass(unittest.TestCase):
    """
    Test case for UnnamedClass
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_UnnamedClass.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of UnnamedClass for testing
        """
        instance = UnnamedClass(
            self_='plvczcatdoyhfsklisjq',
            region='mmlnoyvcilxfekqjjudg',
            station_id='nialtsqrbtiqunnuvgdn'
        )
        return instance

    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'plvczcatdoyhfsklisjq'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'mmlnoyvcilxfekqjjudg'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nialtsqrbtiqunnuvgdn'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = UnnamedClass.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = UnnamedClass.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

