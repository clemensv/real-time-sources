"""
Test case for Measurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gios_poland_producer_data.measurement import Measurement
import datetime


class Test_Measurement(unittest.TestCase):
    """
    Test case for Measurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Measurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Measurement for testing
        """
        instance = Measurement(
            station_id=int(84),
            sensor_id=int(41),
            sensor_code='uxjckrnbootrlftseecz',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(41.276812268222464)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(84)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(41)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_sensor_code_property(self):
        """
        Test sensor_code property
        """
        test_value = 'uxjckrnbootrlftseecz'
        self.instance.sensor_code = test_value
        self.assertEqual(self.instance.sensor_code, test_value)
    
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
        test_value = float(41.276812268222464)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Measurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Measurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

