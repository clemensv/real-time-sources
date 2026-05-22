"""
Test case for OceanObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.oceanobservation import OceanObservation


class Test_OceanObservation(unittest.TestCase):
    """
    Test case for OceanObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_OceanObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OceanObservation for testing
        """
        instance = OceanObservation(
            observation_id='vxkjyylmxadusfhvbvjh',
            station_id='gszvlwmpbmewhglrettt',
            parameter_id='ekupjjwupfkjyrcwyqll',
            observed='yrqvrisfcffqjapfmwic',
            value=float(60.92042654134065),
            latitude=float(98.28252399868575),
            longitude=float(67.21709250700877)
        )
        return instance

    
    def test_observation_id_property(self):
        """
        Test observation_id property
        """
        test_value = 'vxkjyylmxadusfhvbvjh'
        self.instance.observation_id = test_value
        self.assertEqual(self.instance.observation_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'gszvlwmpbmewhglrettt'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = 'ekupjjwupfkjyrcwyqll'
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_observed_property(self):
        """
        Test observed property
        """
        test_value = 'yrqvrisfcffqjapfmwic'
        self.instance.observed = test_value
        self.assertEqual(self.instance.observed, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(60.92042654134065)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(98.28252399868575)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(67.21709250700877)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = OceanObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = OceanObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

