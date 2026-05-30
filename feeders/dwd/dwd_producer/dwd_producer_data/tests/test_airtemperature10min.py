"""
Test case for AirTemperature10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.airtemperature10min import AirTemperature10Min


class Test_AirTemperature10Min(unittest.TestCase):
    """
    Test case for AirTemperature10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AirTemperature10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AirTemperature10Min for testing
        """
        instance = AirTemperature10Min(
            station_id='gdkuktndhpiaaiiqnfql',
            timestamp='uwlqcsurgkprwsqpjhct',
            quality_level=int(16),
            pressure_station_level=float(84.90244971661595),
            air_temperature_2m=float(58.9329974236785),
            air_temperature_5cm=float(95.78392558053304),
            relative_humidity=float(43.048923151962214),
            dew_point_temperature=float(31.529882109160745),
            state='pmieisvblfahickrdbiy'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'gdkuktndhpiaaiiqnfql'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'uwlqcsurgkprwsqpjhct'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(16)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_pressure_station_level_property(self):
        """
        Test pressure_station_level property
        """
        test_value = float(84.90244971661595)
        self.instance.pressure_station_level = test_value
        self.assertEqual(self.instance.pressure_station_level, test_value)
    
    def test_air_temperature_2m_property(self):
        """
        Test air_temperature_2m property
        """
        test_value = float(58.9329974236785)
        self.instance.air_temperature_2m = test_value
        self.assertEqual(self.instance.air_temperature_2m, test_value)
    
    def test_air_temperature_5cm_property(self):
        """
        Test air_temperature_5cm property
        """
        test_value = float(95.78392558053304)
        self.instance.air_temperature_5cm = test_value
        self.assertEqual(self.instance.air_temperature_5cm, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = float(43.048923151962214)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_dew_point_temperature_property(self):
        """
        Test dew_point_temperature property
        """
        test_value = float(31.529882109160745)
        self.instance.dew_point_temperature = test_value
        self.assertEqual(self.instance.dew_point_temperature, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'pmieisvblfahickrdbiy'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AirTemperature10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AirTemperature10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

