"""
Test case for BuoyContinuousWindObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.buoycontinuouswindobservation import BuoyContinuousWindObservation
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
            station_id='owdteynhmydkchgggela',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(88.5699327558729),
            wind_speed=float(53.64378512216672),
            gust_direction=float(84.1770188259074),
            gust=float(92.74734606515142),
            gust_time_code='fzbioyokgnghxnrmcdho',
            region='fyhngibvmyjbmfzrbnpq'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'owdteynhmydkchgggela'
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
        test_value = float(88.5699327558729)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(53.64378512216672)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_direction_property(self):
        """
        Test gust_direction property
        """
        test_value = float(84.1770188259074)
        self.instance.gust_direction = test_value
        self.assertEqual(self.instance.gust_direction, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(92.74734606515142)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_gust_time_code_property(self):
        """
        Test gust_time_code property
        """
        test_value = 'fzbioyokgnghxnrmcdho'
        self.instance.gust_time_code = test_value
        self.assertEqual(self.instance.gust_time_code, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'fyhngibvmyjbmfzrbnpq'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyContinuousWindObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoyContinuousWindObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

