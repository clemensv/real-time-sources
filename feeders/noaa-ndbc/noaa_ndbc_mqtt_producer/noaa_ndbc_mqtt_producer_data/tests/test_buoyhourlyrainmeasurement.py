"""
Test case for BuoyHourlyRainMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_mqtt_producer_data.buoyhourlyrainmeasurement import BuoyHourlyRainMeasurement
import datetime


class Test_BuoyHourlyRainMeasurement(unittest.TestCase):
    """
    Test case for BuoyHourlyRainMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyHourlyRainMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyHourlyRainMeasurement for testing
        """
        instance = BuoyHourlyRainMeasurement(
            station_id='lawihlqygjnoribsyxrj',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            accumulation=float(32.39504043258875),
            region='zrotplsfcdonnhivwjvo'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'lawihlqygjnoribsyxrj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_accumulation_property(self):
        """
        Test accumulation property
        """
        test_value = float(32.39504043258875)
        self.instance.accumulation = test_value
        self.assertEqual(self.instance.accumulation, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'zrotplsfcdonnhivwjvo'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyHourlyRainMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoyHourlyRainMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

