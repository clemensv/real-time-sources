"""
Test case for BuoySupplementalMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoysupplementalmeasurement import BuoySupplementalMeasurement
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
            station_id='egwpsyhiihlfvvlqtsme',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            lowest_pressure=float(93.5442077388202),
            lowest_pressure_time_code='vaplqmcgwkmlcmamobiz',
            highest_wind_speed=float(41.87533293542359),
            highest_wind_direction=float(35.647600348843426),
            highest_wind_time_code='efevvzhbqypzxcruzrwy'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'egwpsyhiihlfvvlqtsme'
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
        test_value = float(93.5442077388202)
        self.instance.lowest_pressure = test_value
        self.assertEqual(self.instance.lowest_pressure, test_value)
    
    def test_lowest_pressure_time_code_property(self):
        """
        Test lowest_pressure_time_code property
        """
        test_value = 'vaplqmcgwkmlcmamobiz'
        self.instance.lowest_pressure_time_code = test_value
        self.assertEqual(self.instance.lowest_pressure_time_code, test_value)
    
    def test_highest_wind_speed_property(self):
        """
        Test highest_wind_speed property
        """
        test_value = float(41.87533293542359)
        self.instance.highest_wind_speed = test_value
        self.assertEqual(self.instance.highest_wind_speed, test_value)
    
    def test_highest_wind_direction_property(self):
        """
        Test highest_wind_direction property
        """
        test_value = float(35.647600348843426)
        self.instance.highest_wind_direction = test_value
        self.assertEqual(self.instance.highest_wind_direction, test_value)
    
    def test_highest_wind_time_code_property(self):
        """
        Test highest_wind_time_code property
        """
        test_value = 'efevvzhbqypzxcruzrwy'
        self.instance.highest_wind_time_code = test_value
        self.assertEqual(self.instance.highest_wind_time_code, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoySupplementalMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
