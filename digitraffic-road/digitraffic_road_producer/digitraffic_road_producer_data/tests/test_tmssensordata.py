"""
Test case for TmsSensorData
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_producer_data.tmssensordata import TmsSensorData


class Test_TmsSensorData(unittest.TestCase):
    """
    Test case for TmsSensorData
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TmsSensorData.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TmsSensorData for testing
        """
        instance = TmsSensorData(
            station_id=int(46),
            sensor_id=int(9),
            value=float(93.22125726948151),
            time=int(10),
            start=int(22),
            end=int(76)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(46)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(9)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(93.22125726948151)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(10)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = int(22)
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = int(76)
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TmsSensorData.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TmsSensorData.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

