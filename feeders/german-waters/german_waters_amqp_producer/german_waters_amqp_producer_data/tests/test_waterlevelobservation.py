"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from german_waters_amqp_producer_data.waterlevelobservation import WaterLevelObservation
import datetime


class Test_WaterLevelObservation(unittest.TestCase):
    """
    Test case for WaterLevelObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevelObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevelObservation for testing
        """
        instance = WaterLevelObservation(
            station_id='xnjeozgbepngprqcyqsu',
            provider='ufdhzlgdhsldhphtzytv',
            water_body='vpuoscqnisxfkrsbalpk',
            water_level=float(18.548681720982017),
            water_level_unit='jzntmeaekqxtyuiqbycq',
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(10.666859593971068),
            discharge_unit='pwzjohbpwkmjjlqrnovh',
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            trend=int(32),
            situation=int(46)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'xnjeozgbepngprqcyqsu'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = 'ufdhzlgdhsldhphtzytv'
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_water_body_property(self):
        """
        Test water_body property
        """
        test_value = 'vpuoscqnisxfkrsbalpk'
        self.instance.water_body = test_value
        self.assertEqual(self.instance.water_body, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(18.548681720982017)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_water_level_unit_property(self):
        """
        Test water_level_unit property
        """
        test_value = 'jzntmeaekqxtyuiqbycq'
        self.instance.water_level_unit = test_value
        self.assertEqual(self.instance.water_level_unit, test_value)
    
    def test_water_level_timestamp_property(self):
        """
        Test water_level_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.water_level_timestamp = test_value
        self.assertEqual(self.instance.water_level_timestamp, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(10.666859593971068)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_discharge_unit_property(self):
        """
        Test discharge_unit property
        """
        test_value = 'pwzjohbpwkmjjlqrnovh'
        self.instance.discharge_unit = test_value
        self.assertEqual(self.instance.discharge_unit, test_value)
    
    def test_discharge_timestamp_property(self):
        """
        Test discharge_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.discharge_timestamp = test_value
        self.assertEqual(self.instance.discharge_timestamp, test_value)
    
    def test_trend_property(self):
        """
        Test trend property
        """
        test_value = int(32)
        self.instance.trend = test_value
        self.assertEqual(self.instance.trend, test_value)
    
    def test_situation_property(self):
        """
        Test situation property
        """
        test_value = int(46)
        self.instance.situation = test_value
        self.assertEqual(self.instance.situation, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevelObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

