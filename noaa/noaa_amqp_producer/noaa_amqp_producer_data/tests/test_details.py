"""
Test case for Details
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_amqp_producer_data.microsoft.opendata.us.noaa.stationtypes.details import Details


class Test_Details(unittest.TestCase):
    """
    Test case for Details
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Details.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Details for testing
        """
        instance = Details(
            self_='tbclfqgnsigapanhfxkz',
            region='ejndugwmefljtlyujqzw',
            station_id='xnqazymttrvzgbmjafjx'
        )
        return instance

    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'tbclfqgnsigapanhfxkz'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'ejndugwmefljtlyujqzw'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'xnqazymttrvzgbmjafjx'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Details.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Details.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

