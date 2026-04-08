"""
Test case for WaterLevelReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.waterlevelreading import WaterLevelReading


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
            station_id='otzipvttjxchagxzfaet',
            title='xjluwdnbobrsbnhosnut',
            basin='bzunrewavxtsliecunua',
            water_level=float(58.27412011201919),
            danger_level=float(57.24216029707806),
            warning_level=float(33.87730508967366),
            status='zovfetywikktqazorkgj',
            trend='batgyzvqujffonvsbair',
            water_level_on='dvridsubkwxqobjgnivj'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'otzipvttjxchagxzfaet'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'xjluwdnbobrsbnhosnut'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'bzunrewavxtsliecunua'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(58.27412011201919)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_danger_level_property(self):
        """
        Test danger_level property
        """
        test_value = float(57.24216029707806)
        self.instance.danger_level = test_value
        self.assertEqual(self.instance.danger_level, test_value)
    
    def test_warning_level_property(self):
        """
        Test warning_level property
        """
        test_value = float(33.87730508967366)
        self.instance.warning_level = test_value
        self.assertEqual(self.instance.warning_level, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'zovfetywikktqazorkgj'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_trend_property(self):
        """
        Test trend property
        """
        test_value = 'batgyzvqujffonvsbair'
        self.instance.trend = test_value
        self.assertEqual(self.instance.trend, test_value)
    
    def test_water_level_on_property(self):
        """
        Test water_level_on property
        """
        test_value = 'dvridsubkwxqobjgnivj'
        self.instance.water_level_on = test_value
        self.assertEqual(self.instance.water_level_on, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
