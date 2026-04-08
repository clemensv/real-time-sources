"""
Test case for BuoyDartMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.buoydartmeasurement import BuoyDartMeasurement
import datetime


class Test_BuoyDartMeasurement(unittest.TestCase):
    """
    Test case for BuoyDartMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyDartMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyDartMeasurement for testing
        """
        instance = BuoyDartMeasurement(
            station_id='xmzkmsqubuwavqfiuuuj',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            measurement_type_code=int(3),
            water_column_height=float(86.12791096019471)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'xmzkmsqubuwavqfiuuuj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_measurement_type_code_property(self):
        """
        Test measurement_type_code property
        """
        test_value = int(3)
        self.instance.measurement_type_code = test_value
        self.assertEqual(self.instance.measurement_type_code, test_value)
    
    def test_water_column_height_property(self):
        """
        Test water_column_height property
        """
        test_value = float(86.12791096019471)
        self.instance.water_column_height = test_value
        self.assertEqual(self.instance.water_column_height, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyDartMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoyDartMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

