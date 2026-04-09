"""
Test case for SnowObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from snotel_producer_data.snowobservation import SnowObservation
import datetime


class Test_SnowObservation(unittest.TestCase):
    """
    Test case for SnowObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SnowObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SnowObservation for testing
        """
        instance = SnowObservation(
            station_triplet='sqppkuirwdsbbclthilm',
            date_time=datetime.datetime.now(datetime.timezone.utc),
            snow_water_equivalent=float(59.806860375272585),
            snow_depth=float(94.76258657827115),
            precipitation=float(20.231901861999766),
            air_temperature=float(55.150797448682894)
        )
        return instance

    
    def test_station_triplet_property(self):
        """
        Test station_triplet property
        """
        test_value = 'sqppkuirwdsbbclthilm'
        self.instance.station_triplet = test_value
        self.assertEqual(self.instance.station_triplet, test_value)
    
    def test_date_time_property(self):
        """
        Test date_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_time = test_value
        self.assertEqual(self.instance.date_time, test_value)
    
    def test_snow_water_equivalent_property(self):
        """
        Test snow_water_equivalent property
        """
        test_value = float(59.806860375272585)
        self.instance.snow_water_equivalent = test_value
        self.assertEqual(self.instance.snow_water_equivalent, test_value)
    
    def test_snow_depth_property(self):
        """
        Test snow_depth property
        """
        test_value = float(94.76258657827115)
        self.instance.snow_depth = test_value
        self.assertEqual(self.instance.snow_depth, test_value)
    
    def test_precipitation_property(self):
        """
        Test precipitation property
        """
        test_value = float(20.231901861999766)
        self.instance.precipitation = test_value
        self.assertEqual(self.instance.precipitation, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(55.150797448682894)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SnowObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SnowObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

