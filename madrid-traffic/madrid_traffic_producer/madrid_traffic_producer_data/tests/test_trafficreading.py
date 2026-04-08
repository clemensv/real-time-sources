"""
Test case for TrafficReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from madrid_traffic_producer_data.trafficreading import TrafficReading
import datetime


class Test_TrafficReading(unittest.TestCase):
    """
    Test case for TrafficReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficReading for testing
        """
        instance = TrafficReading(
            sensor_id='dabsdcvessyauypmntxp',
            intensity=int(13),
            occupancy=int(33),
            load=int(39),
            service_level=int(9),
            error_flag='evphxwabqbwstnsyilir',
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = 'dabsdcvessyauypmntxp'
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_intensity_property(self):
        """
        Test intensity property
        """
        test_value = int(13)
        self.instance.intensity = test_value
        self.assertEqual(self.instance.intensity, test_value)
    
    def test_occupancy_property(self):
        """
        Test occupancy property
        """
        test_value = int(33)
        self.instance.occupancy = test_value
        self.assertEqual(self.instance.occupancy, test_value)
    
    def test_load_property(self):
        """
        Test load property
        """
        test_value = int(39)
        self.instance.load = test_value
        self.assertEqual(self.instance.load, test_value)
    
    def test_service_level_property(self):
        """
        Test service_level property
        """
        test_value = int(9)
        self.instance.service_level = test_value
        self.assertEqual(self.instance.service_level, test_value)
    
    def test_error_flag_property(self):
        """
        Test error_flag property
        """
        test_value = 'evphxwabqbwstnsyilir'
        self.instance.error_flag = test_value
        self.assertEqual(self.instance.error_flag, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

