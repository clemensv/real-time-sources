"""
Test case for BuoyHourlyRainMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoyhourlyrainmeasurement import BuoyHourlyRainMeasurement
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
            station_id='rfdmstkgtexdikwzxthr',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            accumulation=float(18.07001992311076)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'rfdmstkgtexdikwzxthr'
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
        test_value = float(18.07001992311076)
        self.instance.accumulation = test_value
        self.assertEqual(self.instance.accumulation, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyHourlyRainMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
