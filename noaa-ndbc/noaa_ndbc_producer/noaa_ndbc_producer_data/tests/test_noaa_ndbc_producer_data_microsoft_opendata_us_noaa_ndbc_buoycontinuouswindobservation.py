"""
Test case for BuoyContinuousWindObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoycontinuouswindobservation import BuoyContinuousWindObservation
import datetime


class Test_BuoyContinuousWindObservation(unittest.TestCase):
    """
    Test case for BuoyContinuousWindObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyContinuousWindObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyContinuousWindObservation for testing
        """
        instance = BuoyContinuousWindObservation(
            station_id='wkrntmfgknwnsygomlse',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(47.162227680921255),
            wind_speed=float(23.633055325359344),
            gust_direction=float(83.75656076949801),
            gust=float(31.992725210138417),
            gust_time_code='zeohjsjvmvylqkdxmqwt'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'wkrntmfgknwnsygomlse'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(47.162227680921255)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(23.633055325359344)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_direction_property(self):
        """
        Test gust_direction property
        """
        test_value = float(83.75656076949801)
        self.instance.gust_direction = test_value
        self.assertEqual(self.instance.gust_direction, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(31.992725210138417)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_gust_time_code_property(self):
        """
        Test gust_time_code property
        """
        test_value = 'zeohjsjvmvylqkdxmqwt'
        self.instance.gust_time_code = test_value
        self.assertEqual(self.instance.gust_time_code, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyContinuousWindObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
