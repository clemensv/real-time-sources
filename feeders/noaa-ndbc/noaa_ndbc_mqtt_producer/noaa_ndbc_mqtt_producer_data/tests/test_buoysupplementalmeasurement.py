"""
Test case for BuoySupplementalMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_mqtt_producer_data.buoysupplementalmeasurement import BuoySupplementalMeasurement
import datetime


class Test_BuoySupplementalMeasurement(unittest.TestCase):
    """
    Test case for BuoySupplementalMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoySupplementalMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoySupplementalMeasurement for testing
        """
        instance = BuoySupplementalMeasurement(
            station_id='kitbsxqyfovldnfwywbp',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            lowest_pressure=float(37.572541612926656),
            lowest_pressure_time_code='izwdhfjwecxyxrwwrxut',
            highest_wind_speed=float(91.68240945118929),
            highest_wind_direction=float(88.35682521142897),
            highest_wind_time_code='okgfseumalnsdfllrqil',
            region='xhqpfmyprmqpjytbivgt'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'kitbsxqyfovldnfwywbp'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_lowest_pressure_property(self):
        """
        Test lowest_pressure property
        """
        test_value = float(37.572541612926656)
        self.instance.lowest_pressure = test_value
        self.assertEqual(self.instance.lowest_pressure, test_value)
    
    def test_lowest_pressure_time_code_property(self):
        """
        Test lowest_pressure_time_code property
        """
        test_value = 'izwdhfjwecxyxrwwrxut'
        self.instance.lowest_pressure_time_code = test_value
        self.assertEqual(self.instance.lowest_pressure_time_code, test_value)
    
    def test_highest_wind_speed_property(self):
        """
        Test highest_wind_speed property
        """
        test_value = float(91.68240945118929)
        self.instance.highest_wind_speed = test_value
        self.assertEqual(self.instance.highest_wind_speed, test_value)
    
    def test_highest_wind_direction_property(self):
        """
        Test highest_wind_direction property
        """
        test_value = float(88.35682521142897)
        self.instance.highest_wind_direction = test_value
        self.assertEqual(self.instance.highest_wind_direction, test_value)
    
    def test_highest_wind_time_code_property(self):
        """
        Test highest_wind_time_code property
        """
        test_value = 'okgfseumalnsdfllrqil'
        self.instance.highest_wind_time_code = test_value
        self.assertEqual(self.instance.highest_wind_time_code, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'xhqpfmyprmqpjytbivgt'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoySupplementalMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoySupplementalMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

