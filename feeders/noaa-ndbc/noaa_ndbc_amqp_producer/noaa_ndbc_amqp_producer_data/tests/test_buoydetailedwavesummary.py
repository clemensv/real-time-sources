"""
Test case for BuoyDetailedWaveSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_amqp_producer_data.buoydetailedwavesummary import BuoyDetailedWaveSummary
import datetime


class Test_BuoyDetailedWaveSummary(unittest.TestCase):
    """
    Test case for BuoyDetailedWaveSummary
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyDetailedWaveSummary.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyDetailedWaveSummary for testing
        """
        instance = BuoyDetailedWaveSummary(
            station_id='woauifsjbnesgzwaobnw',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            significant_wave_height=float(73.79108918323118),
            swell_height=float(82.15918234469673),
            swell_period=float(6.366060103912963),
            wind_wave_height=float(83.90585556647522),
            wind_wave_period=float(85.39279451691688),
            swell_direction='nrujsmkaqskxckiueiqr',
            wind_wave_direction='kohiprfwrhlpslkwmfdh',
            steepness='yqrxemhbdmugpsomemvy',
            average_wave_period=float(32.1119676061131),
            mean_wave_direction=float(77.80446881801761),
            region='vhdpncgmhnrtktbdjfuj'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'woauifsjbnesgzwaobnw'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_significant_wave_height_property(self):
        """
        Test significant_wave_height property
        """
        test_value = float(73.79108918323118)
        self.instance.significant_wave_height = test_value
        self.assertEqual(self.instance.significant_wave_height, test_value)
    
    def test_swell_height_property(self):
        """
        Test swell_height property
        """
        test_value = float(82.15918234469673)
        self.instance.swell_height = test_value
        self.assertEqual(self.instance.swell_height, test_value)
    
    def test_swell_period_property(self):
        """
        Test swell_period property
        """
        test_value = float(6.366060103912963)
        self.instance.swell_period = test_value
        self.assertEqual(self.instance.swell_period, test_value)
    
    def test_wind_wave_height_property(self):
        """
        Test wind_wave_height property
        """
        test_value = float(83.90585556647522)
        self.instance.wind_wave_height = test_value
        self.assertEqual(self.instance.wind_wave_height, test_value)
    
    def test_wind_wave_period_property(self):
        """
        Test wind_wave_period property
        """
        test_value = float(85.39279451691688)
        self.instance.wind_wave_period = test_value
        self.assertEqual(self.instance.wind_wave_period, test_value)
    
    def test_swell_direction_property(self):
        """
        Test swell_direction property
        """
        test_value = 'nrujsmkaqskxckiueiqr'
        self.instance.swell_direction = test_value
        self.assertEqual(self.instance.swell_direction, test_value)
    
    def test_wind_wave_direction_property(self):
        """
        Test wind_wave_direction property
        """
        test_value = 'kohiprfwrhlpslkwmfdh'
        self.instance.wind_wave_direction = test_value
        self.assertEqual(self.instance.wind_wave_direction, test_value)
    
    def test_steepness_property(self):
        """
        Test steepness property
        """
        test_value = 'yqrxemhbdmugpsomemvy'
        self.instance.steepness = test_value
        self.assertEqual(self.instance.steepness, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(32.1119676061131)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(77.80446881801761)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'vhdpncgmhnrtktbdjfuj'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyDetailedWaveSummary.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoyDetailedWaveSummary.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

