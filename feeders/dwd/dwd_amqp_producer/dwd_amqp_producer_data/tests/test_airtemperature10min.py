"""
Test case for AirTemperature10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_amqp_producer_data.airtemperature10min import AirTemperature10Min


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
            station_id='fevsadurrtzpaznpizrv',
            timestamp='wsuumuungkstsjerrxsl',
            quality_level=int(40),
            pressure_station_level=float(77.81963222017441),
            air_temperature_2m=float(79.16532795606038),
            air_temperature_5cm=float(78.3699739245586),
            relative_humidity=float(2.1699494709148004),
            dew_point_temperature=float(17.84514899289875),
            state='paweqwkpphguprropfko'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fevsadurrtzpaznpizrv'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'wsuumuungkstsjerrxsl'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(40)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_pressure_station_level_property(self):
        """
        Test pressure_station_level property
        """
        test_value = float(77.81963222017441)
        self.instance.pressure_station_level = test_value
        self.assertEqual(self.instance.pressure_station_level, test_value)
    
    def test_air_temperature_2m_property(self):
        """
        Test air_temperature_2m property
        """
        test_value = float(79.16532795606038)
        self.instance.air_temperature_2m = test_value
        self.assertEqual(self.instance.air_temperature_2m, test_value)
    
    def test_air_temperature_5cm_property(self):
        """
        Test air_temperature_5cm property
        """
        test_value = float(78.3699739245586)
        self.instance.air_temperature_5cm = test_value
        self.assertEqual(self.instance.air_temperature_5cm, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = float(2.1699494709148004)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_dew_point_temperature_property(self):
        """
        Test dew_point_temperature property
        """
        test_value = float(17.84514899289875)
        self.instance.dew_point_temperature = test_value
        self.assertEqual(self.instance.dew_point_temperature, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'paweqwkpphguprropfko'
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

