"""
Test case for PlanetaryKIndex
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.planetarykindex import PlanetaryKIndex


class Test_PlanetaryKIndex(unittest.TestCase):
    """
    Test case for PlanetaryKIndex
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PlanetaryKIndex.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PlanetaryKIndex for testing
        """
        instance = PlanetaryKIndex(
            observation_time='jwqqkwsdzuiltamlnrqj',
            kp=float(49.57935707276761),
            a_running=float(53.833403000016546),
            station_count=int(44)
        )
        return instance

    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'jwqqkwsdzuiltamlnrqj'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_kp_property(self):
        """
        Test kp property
        """
        test_value = float(49.57935707276761)
        self.instance.kp = test_value
        self.assertEqual(self.instance.kp, test_value)
    
    def test_a_running_property(self):
        """
        Test a_running property
        """
        test_value = float(53.833403000016546)
        self.instance.a_running = test_value
        self.assertEqual(self.instance.a_running, test_value)
    
    def test_station_count_property(self):
        """
        Test station_count property
        """
        test_value = int(44)
        self.instance.station_count = test_value
        self.assertEqual(self.instance.station_count, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PlanetaryKIndex.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PlanetaryKIndex.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

