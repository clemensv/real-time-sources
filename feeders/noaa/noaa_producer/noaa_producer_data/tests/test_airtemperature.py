"""
Test case for AirTemperature
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.airtemperature import AirTemperature


class Test_AirTemperature(unittest.TestCase):
    """
    Test case for AirTemperature
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AirTemperature.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AirTemperature for testing
        """
        instance = AirTemperature(
            station_id='fvqxhggayicrrjuvdyou',
            timestamp='hkktqzenfygnelstglgq',
            value=float(12.603691454891697),
            max_temp_exceeded=False,
            min_temp_exceeded=False,
            rate_of_change_exceeded=False,
            region='lemkzeltvrcfnktbilzg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fvqxhggayicrrjuvdyou'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'hkktqzenfygnelstglgq'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(12.603691454891697)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_max_temp_exceeded_property(self):
        """
        Test max_temp_exceeded property
        """
        test_value = False
        self.instance.max_temp_exceeded = test_value
        self.assertEqual(self.instance.max_temp_exceeded, test_value)
    
    def test_min_temp_exceeded_property(self):
        """
        Test min_temp_exceeded property
        """
        test_value = False
        self.instance.min_temp_exceeded = test_value
        self.assertEqual(self.instance.min_temp_exceeded, test_value)
    
    def test_rate_of_change_exceeded_property(self):
        """
        Test rate_of_change_exceeded property
        """
        test_value = False
        self.instance.rate_of_change_exceeded = test_value
        self.assertEqual(self.instance.rate_of_change_exceeded, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'lemkzeltvrcfnktbilzg'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AirTemperature.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AirTemperature.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

