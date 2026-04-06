"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from german_waters_producer_data.de.waters.hydrology.waterlevelobservation import WaterLevelObservation
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
            station_id='moqjxqutquardqqgaflb',
            provider='gakqnkpfaxaxlsiadshe',
            water_level=float(59.649982729857484),
            water_level_unit='dpmymwgmvsjdlxxajzqc',
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(28.65918097624469),
            discharge_unit='knawnedidtsegrdtpzgf',
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            trend=int(77),
            situation=int(23)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'moqjxqutquardqqgaflb'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = 'gakqnkpfaxaxlsiadshe'
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(59.649982729857484)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_water_level_unit_property(self):
        """
        Test water_level_unit property
        """
        test_value = 'dpmymwgmvsjdlxxajzqc'
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
        test_value = float(28.65918097624469)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_discharge_unit_property(self):
        """
        Test discharge_unit property
        """
        test_value = 'knawnedidtsegrdtpzgf'
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
        test_value = int(77)
        self.instance.trend = test_value
        self.assertEqual(self.instance.trend, test_value)
    
    def test_situation_property(self):
        """
        Test situation property
        """
        test_value = int(23)
        self.instance.situation = test_value
        self.assertEqual(self.instance.situation, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
