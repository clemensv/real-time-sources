"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bafu_hydro_amqp_producer_data.waterlevelobservation import WaterLevelObservation
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
            station_id='lycfzyhweyyfkbhmrhqs',
            water_body_name='ivrtyjwbnmdwznjbqudw',
            water_level=float(40.07464742638637),
            water_level_unit='suvbxqfljylqdywbkgxo',
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(24.34084013657294),
            discharge_unit='jkvttldjiqxvjqmqtaeg',
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            water_temperature=float(27.19569715532979),
            water_temperature_unit='updpqqaqtgpjxfmqibzj',
            water_temperature_timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'lycfzyhweyyfkbhmrhqs'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_water_body_name_property(self):
        """
        Test water_body_name property
        """
        test_value = 'ivrtyjwbnmdwznjbqudw'
        self.instance.water_body_name = test_value
        self.assertEqual(self.instance.water_body_name, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(40.07464742638637)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_water_level_unit_property(self):
        """
        Test water_level_unit property
        """
        test_value = 'suvbxqfljylqdywbkgxo'
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
        test_value = float(24.34084013657294)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_discharge_unit_property(self):
        """
        Test discharge_unit property
        """
        test_value = 'jkvttldjiqxvjqmqtaeg'
        self.instance.discharge_unit = test_value
        self.assertEqual(self.instance.discharge_unit, test_value)
    
    def test_discharge_timestamp_property(self):
        """
        Test discharge_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.discharge_timestamp = test_value
        self.assertEqual(self.instance.discharge_timestamp, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(27.19569715532979)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_water_temperature_unit_property(self):
        """
        Test water_temperature_unit property
        """
        test_value = 'updpqqaqtgpjxfmqibzj'
        self.instance.water_temperature_unit = test_value
        self.assertEqual(self.instance.water_temperature_unit, test_value)
    
    def test_water_temperature_timestamp_property(self):
        """
        Test water_temperature_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.water_temperature_timestamp = test_value
        self.assertEqual(self.instance.water_temperature_timestamp, test_value)
    
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

