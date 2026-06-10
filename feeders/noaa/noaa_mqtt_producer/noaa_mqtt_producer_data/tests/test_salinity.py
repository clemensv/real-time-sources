"""
Test case for Salinity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_mqtt_producer_data.microsoft.opendata.us.noaa.salinity import Salinity


class Test_Salinity(unittest.TestCase):
    """
    Test case for Salinity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Salinity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Salinity for testing
        """
        instance = Salinity(
            station_id='hobvumkzqenaxdjmuqyd',
            timestamp='buoumvpquvnhzmwqbgno',
            salinity=float(65.21876174921728),
            grams_per_kg=float(85.87231994878202),
            region='vqmpvfyjaqfwlndyurgn'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'hobvumkzqenaxdjmuqyd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'buoumvpquvnhzmwqbgno'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_salinity_property(self):
        """
        Test salinity property
        """
        test_value = float(65.21876174921728)
        self.instance.salinity = test_value
        self.assertEqual(self.instance.salinity, test_value)
    
    def test_grams_per_kg_property(self):
        """
        Test grams_per_kg property
        """
        test_value = float(85.87231994878202)
        self.instance.grams_per_kg = test_value
        self.assertEqual(self.instance.grams_per_kg, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'vqmpvfyjaqfwlndyurgn'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Salinity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Salinity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

