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
            station_id='wlmqssncolkoncdnjhee',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            significant_wave_height=float(22.764215688409383),
            swell_height=float(20.52196038377011),
            swell_period=float(51.24099976368288),
            wind_wave_height=float(85.88117478363117),
            wind_wave_period=float(15.179801095761658),
            swell_direction='jrsgdqsqtnzvhwhmwhcc',
            wind_wave_direction='fpgiqsulcoqwhhpkvxga',
            steepness='ngbogateabgnddhizuvs',
            average_wave_period=float(35.34570288277279),
            mean_wave_direction=float(46.37667185452145),
            region='uveeobvtretsnioojbly'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'wlmqssncolkoncdnjhee'
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
        test_value = float(22.764215688409383)
        self.instance.significant_wave_height = test_value
        self.assertEqual(self.instance.significant_wave_height, test_value)
    
    def test_swell_height_property(self):
        """
        Test swell_height property
        """
        test_value = float(20.52196038377011)
        self.instance.swell_height = test_value
        self.assertEqual(self.instance.swell_height, test_value)
    
    def test_swell_period_property(self):
        """
        Test swell_period property
        """
        test_value = float(51.24099976368288)
        self.instance.swell_period = test_value
        self.assertEqual(self.instance.swell_period, test_value)
    
    def test_wind_wave_height_property(self):
        """
        Test wind_wave_height property
        """
        test_value = float(85.88117478363117)
        self.instance.wind_wave_height = test_value
        self.assertEqual(self.instance.wind_wave_height, test_value)
    
    def test_wind_wave_period_property(self):
        """
        Test wind_wave_period property
        """
        test_value = float(15.179801095761658)
        self.instance.wind_wave_period = test_value
        self.assertEqual(self.instance.wind_wave_period, test_value)
    
    def test_swell_direction_property(self):
        """
        Test swell_direction property
        """
        test_value = 'jrsgdqsqtnzvhwhmwhcc'
        self.instance.swell_direction = test_value
        self.assertEqual(self.instance.swell_direction, test_value)
    
    def test_wind_wave_direction_property(self):
        """
        Test wind_wave_direction property
        """
        test_value = 'fpgiqsulcoqwhhpkvxga'
        self.instance.wind_wave_direction = test_value
        self.assertEqual(self.instance.wind_wave_direction, test_value)
    
    def test_steepness_property(self):
        """
        Test steepness property
        """
        test_value = 'ngbogateabgnddhizuvs'
        self.instance.steepness = test_value
        self.assertEqual(self.instance.steepness, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(35.34570288277279)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(46.37667185452145)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'uveeobvtretsnioojbly'
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

