"""
Test case for Solar10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_mqtt_producer_data.solar10min import Solar10Min


class Test_Solar10Min(unittest.TestCase):
    """
    Test case for Solar10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Solar10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Solar10Min for testing
        """
        instance = Solar10Min(
            station_id='nfeusyleaowapeeibklg',
            timestamp='hemslgzqpjrcbbyjykqb',
            quality_level=int(34),
            global_radiation=float(0.43005677937155706),
            sunshine_duration=float(80.9799442031797),
            diffuse_radiation=float(13.944996142603582),
            longwave_radiation=float(70.39921860837171),
            state='uikefwydrpnjtxvvunyc'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nfeusyleaowapeeibklg'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'hemslgzqpjrcbbyjykqb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(34)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_global_radiation_property(self):
        """
        Test global_radiation property
        """
        test_value = float(0.43005677937155706)
        self.instance.global_radiation = test_value
        self.assertEqual(self.instance.global_radiation, test_value)
    
    def test_sunshine_duration_property(self):
        """
        Test sunshine_duration property
        """
        test_value = float(80.9799442031797)
        self.instance.sunshine_duration = test_value
        self.assertEqual(self.instance.sunshine_duration, test_value)
    
    def test_diffuse_radiation_property(self):
        """
        Test diffuse_radiation property
        """
        test_value = float(13.944996142603582)
        self.instance.diffuse_radiation = test_value
        self.assertEqual(self.instance.diffuse_radiation, test_value)
    
    def test_longwave_radiation_property(self):
        """
        Test longwave_radiation property
        """
        test_value = float(70.39921860837171)
        self.instance.longwave_radiation = test_value
        self.assertEqual(self.instance.longwave_radiation, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'uikefwydrpnjtxvvunyc'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Solar10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Solar10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

