"""
Test case for ExtremeWind10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_mqtt_producer_data.extremewind10min import ExtremeWind10Min


class Test_ExtremeWind10Min(unittest.TestCase):
    """
    Test case for ExtremeWind10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ExtremeWind10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ExtremeWind10Min for testing
        """
        instance = ExtremeWind10Min(
            station_id='tvdijsnyztkyryikfppp',
            timestamp='twoumyttdieikrmtfjkg',
            quality_level=int(94),
            wind_speed_maximum=float(79.73279895969097),
            wind_speed_minimum=float(93.87446457380675),
            wind_direction_at_maximum=float(11.406405775509509),
            state='spfhsygzeknpcrxnusrc'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tvdijsnyztkyryikfppp'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'twoumyttdieikrmtfjkg'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(94)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_wind_speed_maximum_property(self):
        """
        Test wind_speed_maximum property
        """
        test_value = float(79.73279895969097)
        self.instance.wind_speed_maximum = test_value
        self.assertEqual(self.instance.wind_speed_maximum, test_value)
    
    def test_wind_speed_minimum_property(self):
        """
        Test wind_speed_minimum property
        """
        test_value = float(93.87446457380675)
        self.instance.wind_speed_minimum = test_value
        self.assertEqual(self.instance.wind_speed_minimum, test_value)
    
    def test_wind_direction_at_maximum_property(self):
        """
        Test wind_direction_at_maximum property
        """
        test_value = float(11.406405775509509)
        self.instance.wind_direction_at_maximum = test_value
        self.assertEqual(self.instance.wind_direction_at_maximum, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'spfhsygzeknpcrxnusrc'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ExtremeWind10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ExtremeWind10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

