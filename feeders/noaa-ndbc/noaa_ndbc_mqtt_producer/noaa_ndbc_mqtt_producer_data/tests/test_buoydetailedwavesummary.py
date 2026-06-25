"""
Test case for BuoyDetailedWaveSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_mqtt_producer_data.buoydetailedwavesummary import BuoyDetailedWaveSummary
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
            station_id='pbxcqtqphqkpqdtaouew',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            significant_wave_height=float(39.62493510035204),
            swell_height=float(98.91202236455301),
            swell_period=float(64.69955644033173),
            wind_wave_height=float(49.688110602486354),
            wind_wave_period=float(65.26792327213376),
            swell_direction='ykwymxpinibjhrdcdvsa',
            wind_wave_direction='qudqznwjdnkzlrtslhcf',
            steepness='fnyebrtidbsctgyslpfp',
            average_wave_period=float(84.61165743430938),
            mean_wave_direction=float(90.69155897574674),
            region='iwqttpsktjpjvigljhgk'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'pbxcqtqphqkpqdtaouew'
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
        test_value = float(39.62493510035204)
        self.instance.significant_wave_height = test_value
        self.assertEqual(self.instance.significant_wave_height, test_value)
    
    def test_swell_height_property(self):
        """
        Test swell_height property
        """
        test_value = float(98.91202236455301)
        self.instance.swell_height = test_value
        self.assertEqual(self.instance.swell_height, test_value)
    
    def test_swell_period_property(self):
        """
        Test swell_period property
        """
        test_value = float(64.69955644033173)
        self.instance.swell_period = test_value
        self.assertEqual(self.instance.swell_period, test_value)
    
    def test_wind_wave_height_property(self):
        """
        Test wind_wave_height property
        """
        test_value = float(49.688110602486354)
        self.instance.wind_wave_height = test_value
        self.assertEqual(self.instance.wind_wave_height, test_value)
    
    def test_wind_wave_period_property(self):
        """
        Test wind_wave_period property
        """
        test_value = float(65.26792327213376)
        self.instance.wind_wave_period = test_value
        self.assertEqual(self.instance.wind_wave_period, test_value)
    
    def test_swell_direction_property(self):
        """
        Test swell_direction property
        """
        test_value = 'ykwymxpinibjhrdcdvsa'
        self.instance.swell_direction = test_value
        self.assertEqual(self.instance.swell_direction, test_value)
    
    def test_wind_wave_direction_property(self):
        """
        Test wind_wave_direction property
        """
        test_value = 'qudqznwjdnkzlrtslhcf'
        self.instance.wind_wave_direction = test_value
        self.assertEqual(self.instance.wind_wave_direction, test_value)
    
    def test_steepness_property(self):
        """
        Test steepness property
        """
        test_value = 'fnyebrtidbsctgyslpfp'
        self.instance.steepness = test_value
        self.assertEqual(self.instance.steepness, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(84.61165743430938)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(90.69155897574674)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'iwqttpsktjpjvigljhgk'
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

