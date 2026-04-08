"""
Test case for BuoyDetailedWaveSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.buoydetailedwavesummary import BuoyDetailedWaveSummary
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
            station_id='ztamrufjdimurwcydueq',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            significant_wave_height=float(26.465562577907555),
            swell_height=float(18.77930655433494),
            swell_period=float(58.26616805061582),
            wind_wave_height=float(46.13613255977547),
            wind_wave_period=float(63.75338594321784),
            swell_direction='zmnbnhbkxpessudfgdii',
            wind_wave_direction='bhcxkoffiprerohqhneg',
            steepness='hercrrlcvkatrqqnrrpf',
            average_wave_period=float(52.95293399179872),
            mean_wave_direction=float(68.82114531415931)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ztamrufjdimurwcydueq'
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
        test_value = float(26.465562577907555)
        self.instance.significant_wave_height = test_value
        self.assertEqual(self.instance.significant_wave_height, test_value)
    
    def test_swell_height_property(self):
        """
        Test swell_height property
        """
        test_value = float(18.77930655433494)
        self.instance.swell_height = test_value
        self.assertEqual(self.instance.swell_height, test_value)
    
    def test_swell_period_property(self):
        """
        Test swell_period property
        """
        test_value = float(58.26616805061582)
        self.instance.swell_period = test_value
        self.assertEqual(self.instance.swell_period, test_value)
    
    def test_wind_wave_height_property(self):
        """
        Test wind_wave_height property
        """
        test_value = float(46.13613255977547)
        self.instance.wind_wave_height = test_value
        self.assertEqual(self.instance.wind_wave_height, test_value)
    
    def test_wind_wave_period_property(self):
        """
        Test wind_wave_period property
        """
        test_value = float(63.75338594321784)
        self.instance.wind_wave_period = test_value
        self.assertEqual(self.instance.wind_wave_period, test_value)
    
    def test_swell_direction_property(self):
        """
        Test swell_direction property
        """
        test_value = 'zmnbnhbkxpessudfgdii'
        self.instance.swell_direction = test_value
        self.assertEqual(self.instance.swell_direction, test_value)
    
    def test_wind_wave_direction_property(self):
        """
        Test wind_wave_direction property
        """
        test_value = 'bhcxkoffiprerohqhneg'
        self.instance.wind_wave_direction = test_value
        self.assertEqual(self.instance.wind_wave_direction, test_value)
    
    def test_steepness_property(self):
        """
        Test steepness property
        """
        test_value = 'hercrrlcvkatrqqnrrpf'
        self.instance.steepness = test_value
        self.assertEqual(self.instance.steepness, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(52.95293399179872)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(68.82114531415931)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
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

