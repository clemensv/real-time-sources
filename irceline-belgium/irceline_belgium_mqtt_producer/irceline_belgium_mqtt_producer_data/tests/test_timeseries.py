"""
Test case for Timeseries
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irceline_belgium_mqtt_producer_data.timeseries import Timeseries
from typing import Any


class Test_Timeseries(unittest.TestCase):
    """
    Test case for Timeseries
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Timeseries.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Timeseries for testing
        """
        instance = Timeseries(
            timeseries_id='rrdmejqkxvshbavsflki',
            label='tfhidoitpzbyytntomke',
            uom='phktdafsosncfawdqujt',
            station_id='tytnsbrrclgckrejndko',
            station_label='zicrdgvxycbsilqfzxle',
            latitude=float(89.64128151226973),
            longitude=float(68.25052537276072),
            phenomenon_id='rfjlleznxpmyxsjfholr',
            phenomenon_label='gpsguwqxyyiokjrcwnat',
            category_id='onzxioojglbzyiavxewg',
            category_label='akrkfvcmotfdfeuqhiaa',
            status_intervals=None
        )
        return instance

    
    def test_timeseries_id_property(self):
        """
        Test timeseries_id property
        """
        test_value = 'rrdmejqkxvshbavsflki'
        self.instance.timeseries_id = test_value
        self.assertEqual(self.instance.timeseries_id, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'tfhidoitpzbyytntomke'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_uom_property(self):
        """
        Test uom property
        """
        test_value = 'phktdafsosncfawdqujt'
        self.instance.uom = test_value
        self.assertEqual(self.instance.uom, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tytnsbrrclgckrejndko'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_label_property(self):
        """
        Test station_label property
        """
        test_value = 'zicrdgvxycbsilqfzxle'
        self.instance.station_label = test_value
        self.assertEqual(self.instance.station_label, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(89.64128151226973)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(68.25052537276072)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_phenomenon_id_property(self):
        """
        Test phenomenon_id property
        """
        test_value = 'rfjlleznxpmyxsjfholr'
        self.instance.phenomenon_id = test_value
        self.assertEqual(self.instance.phenomenon_id, test_value)
    
    def test_phenomenon_label_property(self):
        """
        Test phenomenon_label property
        """
        test_value = 'gpsguwqxyyiokjrcwnat'
        self.instance.phenomenon_label = test_value
        self.assertEqual(self.instance.phenomenon_label, test_value)
    
    def test_category_id_property(self):
        """
        Test category_id property
        """
        test_value = 'onzxioojglbzyiavxewg'
        self.instance.category_id = test_value
        self.assertEqual(self.instance.category_id, test_value)
    
    def test_category_label_property(self):
        """
        Test category_label property
        """
        test_value = 'akrkfvcmotfdfeuqhiaa'
        self.instance.category_label = test_value
        self.assertEqual(self.instance.category_label, test_value)
    
    def test_status_intervals_property(self):
        """
        Test status_intervals property
        """
        test_value = None
        self.instance.status_intervals = test_value
        self.assertEqual(self.instance.status_intervals, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Timeseries.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Timeseries.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

