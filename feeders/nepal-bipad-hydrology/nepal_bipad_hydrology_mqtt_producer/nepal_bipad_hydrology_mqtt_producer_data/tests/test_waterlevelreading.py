"""
Test case for WaterLevelReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nepal_bipad_hydrology_mqtt_producer_data.np.gov.bipad.hydrology.waterlevelreading import WaterLevelReading


class Test_WaterLevelReading(unittest.TestCase):
    """
    Test case for WaterLevelReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevelReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevelReading for testing
        """
        instance = WaterLevelReading(
            station_id='bzizwmhkvgqdwqjnlerz',
            title='rkizazbidmhrlgtkykns',
            basin='buzkbjjveddmsfuncsbe',
            water_level=float(55.59776218840713),
            danger_level=float(33.14168163553196),
            warning_level=float(46.769504835690945),
            status='trvcmggpvypsedsjggng',
            trend='riwfexosedhlchnuflon',
            water_level_on='xwpnjmbwinicffcevlvt'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'bzizwmhkvgqdwqjnlerz'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'rkizazbidmhrlgtkykns'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'buzkbjjveddmsfuncsbe'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(55.59776218840713)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_danger_level_property(self):
        """
        Test danger_level property
        """
        test_value = float(33.14168163553196)
        self.instance.danger_level = test_value
        self.assertEqual(self.instance.danger_level, test_value)
    
    def test_warning_level_property(self):
        """
        Test warning_level property
        """
        test_value = float(46.769504835690945)
        self.instance.warning_level = test_value
        self.assertEqual(self.instance.warning_level, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'trvcmggpvypsedsjggng'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_trend_property(self):
        """
        Test trend property
        """
        test_value = 'riwfexosedhlchnuflon'
        self.instance.trend = test_value
        self.assertEqual(self.instance.trend, test_value)
    
    def test_water_level_on_property(self):
        """
        Test water_level_on property
        """
        test_value = 'xwpnjmbwinicffcevlvt'
        self.instance.water_level_on = test_value
        self.assertEqual(self.instance.water_level_on, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevelReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

