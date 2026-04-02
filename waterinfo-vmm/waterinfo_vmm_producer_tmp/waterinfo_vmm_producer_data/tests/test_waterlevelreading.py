"""
Test case for WaterLevelReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from waterinfo_vmm_producer_data.waterlevelreading import WaterLevelReading
import datetime


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
            ts_id='urbkkoouhjjyrxdfcnjh',
            station_no='omlejhkbdlroregkkceo',
            station_name='suxzpcmcpyxdeclpyxrt',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(39.29341686624947),
            unit_name='svwzbmakuctwracwfnxk',
            parameter_name='hgakjmlmqslwxgpgrwav'
        )
        return instance

    
    def test_ts_id_property(self):
        """
        Test ts_id property
        """
        test_value = 'urbkkoouhjjyrxdfcnjh'
        self.instance.ts_id = test_value
        self.assertEqual(self.instance.ts_id, test_value)
    
    def test_station_no_property(self):
        """
        Test station_no property
        """
        test_value = 'omlejhkbdlroregkkceo'
        self.instance.station_no = test_value
        self.assertEqual(self.instance.station_no, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'suxzpcmcpyxdeclpyxrt'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(39.29341686624947)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_name_property(self):
        """
        Test unit_name property
        """
        test_value = 'svwzbmakuctwracwfnxk'
        self.instance.unit_name = test_value
        self.assertEqual(self.instance.unit_name, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'hgakjmlmqslwxgpgrwav'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
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

