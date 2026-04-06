"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from german_waters_producer_data.waterlevelobservation import WaterLevelObservation
import datetime


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
            station_id='aehuuaatqlknyyxzccho',
            provider='yiotmvpvifhddgdyrzer',
            water_level=float(90.71112163779087),
            water_level_unit='icolvuuiluaybadgxyai',
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(14.040679514173704),
            discharge_unit='uuvccfeaxvgjswqgwkbc',
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            trend=int(66),
            situation=int(65)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'aehuuaatqlknyyxzccho'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = 'yiotmvpvifhddgdyrzer'
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(90.71112163779087)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_water_level_unit_property(self):
        """
        Test water_level_unit property
        """
        test_value = 'icolvuuiluaybadgxyai'
        self.instance.water_level_unit = test_value
        self.assertEqual(self.instance.water_level_unit, test_value)
    
    def test_water_level_timestamp_property(self):
        """
        Test water_level_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.water_level_timestamp = test_value
        self.assertEqual(self.instance.water_level_timestamp, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(14.040679514173704)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_discharge_unit_property(self):
        """
        Test discharge_unit property
        """
        test_value = 'uuvccfeaxvgjswqgwkbc'
        self.instance.discharge_unit = test_value
        self.assertEqual(self.instance.discharge_unit, test_value)
    
    def test_discharge_timestamp_property(self):
        """
        Test discharge_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
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
        test_value = int(65)
        self.instance.situation = test_value
        self.assertEqual(self.instance.situation, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevelObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

