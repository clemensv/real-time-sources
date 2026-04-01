"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from german_waters_producer_data.de.waters.hydrology.waterlevelobservation import WaterLevelObservation


class Test_WaterLevelObservation(unittest.TestCase):
    """
    Test case for WaterLevelObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevelObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevelObservation for testing
        """
        instance = WaterLevelObservation(
            station_id='hqpgptjousatljwmxrmp',
            provider='bscmyqzgphyofqmhytdv',
            water_level=float(36.595958134305874),
            water_level_unit='bbotbpzfewqwrpntruld',
            water_level_timestamp='gwukgtpbbuneyaxrkbvt',
            discharge=float(51.21826713283196),
            discharge_unit='ndxlraxyzdczirxhqjbm',
            discharge_timestamp='zxlitktnoqmnnykkdslp',
            trend=int(66),
            situation=int(19)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'hqpgptjousatljwmxrmp'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = 'bscmyqzgphyofqmhytdv'
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(36.595958134305874)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_water_level_unit_property(self):
        """
        Test water_level_unit property
        """
        test_value = 'bbotbpzfewqwrpntruld'
        self.instance.water_level_unit = test_value
        self.assertEqual(self.instance.water_level_unit, test_value)
    
    def test_water_level_timestamp_property(self):
        """
        Test water_level_timestamp property
        """
        test_value = 'gwukgtpbbuneyaxrkbvt'
        self.instance.water_level_timestamp = test_value
        self.assertEqual(self.instance.water_level_timestamp, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(51.21826713283196)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_discharge_unit_property(self):
        """
        Test discharge_unit property
        """
        test_value = 'ndxlraxyzdczirxhqjbm'
        self.instance.discharge_unit = test_value
        self.assertEqual(self.instance.discharge_unit, test_value)
    
    def test_discharge_timestamp_property(self):
        """
        Test discharge_timestamp property
        """
        test_value = 'zxlitktnoqmnnykkdslp'
        self.instance.discharge_timestamp = test_value
        self.assertEqual(self.instance.discharge_timestamp, test_value)
    
    def test_trend_property(self):
        """
        Test trend property
        """
        test_value = int(66)
        self.instance.trend = test_value
        self.assertEqual(self.instance.trend, test_value)
    
    def test_situation_property(self):
        """
        Test situation property
        """
        test_value = int(19)
        self.instance.situation = test_value
        self.assertEqual(self.instance.situation, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
