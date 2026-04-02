"""
Test case for Wind10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.de.dwd.cdc.wind10min import Wind10Min


class Test_Wind10Min(unittest.TestCase):
    """
    Test case for Wind10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Wind10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Wind10Min for testing
        """
        instance = Wind10Min(
            station_id='kvmbbvpyiqocyrvycqwd',
            timestamp='zszdxicayloxxujubigu',
            quality_level=int(7),
            wind_speed=float(88.58590235158128),
            wind_direction=float(27.97089743346418)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'kvmbbvpyiqocyrvycqwd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'zszdxicayloxxujubigu'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(7)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(88.58590235158128)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(27.97089743346418)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Wind10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
