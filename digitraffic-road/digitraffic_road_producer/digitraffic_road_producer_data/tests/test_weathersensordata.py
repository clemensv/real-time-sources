"""
Test case for WeatherSensorData
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_producer_data.weathersensordata import WeatherSensorData


class Test_WeatherSensorData(unittest.TestCase):
    """
    Test case for WeatherSensorData
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherSensorData.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherSensorData for testing
        """
        instance = WeatherSensorData(
            station_id=int(61),
            sensor_id=int(28),
            value=float(6.07450504321152),
            time=int(96)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(61)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(28)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(6.07450504321152)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(96)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherSensorData.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherSensorData.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

