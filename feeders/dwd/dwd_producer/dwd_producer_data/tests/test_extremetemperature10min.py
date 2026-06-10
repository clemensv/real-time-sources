"""
Test case for ExtremeTemperature10Min
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.extremetemperature10min import ExtremeTemperature10Min


class Test_ExtremeTemperature10Min(unittest.TestCase):
    """
    Test case for ExtremeTemperature10Min
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ExtremeTemperature10Min.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ExtremeTemperature10Min for testing
        """
        instance = ExtremeTemperature10Min(
            station_id='bsedwxsrcsobqctnpuhm',
            timestamp='tlsusteuyfcazhcoruoo',
            quality_level=int(69),
            air_temperature_maximum_2m=float(20.105772158219516),
            air_temperature_minimum_5cm=float(10.612685257679267),
            state='pcdvwwkdtgmulrewaknz'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'bsedwxsrcsobqctnpuhm'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'tlsusteuyfcazhcoruoo'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(69)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_air_temperature_maximum_2m_property(self):
        """
        Test air_temperature_maximum_2m property
        """
        test_value = float(20.105772158219516)
        self.instance.air_temperature_maximum_2m = test_value
        self.assertEqual(self.instance.air_temperature_maximum_2m, test_value)
    
    def test_air_temperature_minimum_5cm_property(self):
        """
        Test air_temperature_minimum_5cm property
        """
        test_value = float(10.612685257679267)
        self.instance.air_temperature_minimum_5cm = test_value
        self.assertEqual(self.instance.air_temperature_minimum_5cm, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'pcdvwwkdtgmulrewaknz'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ExtremeTemperature10Min.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ExtremeTemperature10Min.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

