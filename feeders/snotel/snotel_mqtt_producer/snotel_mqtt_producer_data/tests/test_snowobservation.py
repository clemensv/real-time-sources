"""
Test case for SnowObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from snotel_mqtt_producer_data.snowobservation import SnowObservation
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
            station_triplet='mzekyouqzrsmrgbyugmo',
            date_time=datetime.datetime.now(datetime.timezone.utc),
            snow_water_equivalent=float(30.61719700914133),
            snow_depth=float(36.38339346440973),
            precipitation=float(68.22062084504698),
            air_temperature=float(3.301500034852356),
            state='fxusdgbmafxmqvpwluwi'
        )
        return instance

    
    def test_station_triplet_property(self):
        """
        Test station_triplet property
        """
        test_value = 'mzekyouqzrsmrgbyugmo'
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
        test_value = float(30.61719700914133)
        self.instance.snow_water_equivalent = test_value
        self.assertEqual(self.instance.snow_water_equivalent, test_value)
    
    def test_snow_depth_property(self):
        """
        Test snow_depth property
        """
        test_value = float(36.38339346440973)
        self.instance.snow_depth = test_value
        self.assertEqual(self.instance.snow_depth, test_value)
    
    def test_precipitation_property(self):
        """
        Test precipitation property
        """
        test_value = float(68.22062084504698)
        self.instance.precipitation = test_value
        self.assertEqual(self.instance.precipitation, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(3.301500034852356)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'fxusdgbmafxmqvpwluwi'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
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

