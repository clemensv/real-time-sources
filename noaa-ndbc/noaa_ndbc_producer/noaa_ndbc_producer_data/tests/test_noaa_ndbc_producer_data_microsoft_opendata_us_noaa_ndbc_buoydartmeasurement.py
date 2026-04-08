"""
Test case for BuoyDartMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoydartmeasurement import BuoyDartMeasurement
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
            station_id='ayxbeogjixvprvinryhn',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            measurement_type_code=int(42),
            water_column_height=float(82.38272141564141)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ayxbeogjixvprvinryhn'
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
        test_value = int(42)
        self.instance.measurement_type_code = test_value
        self.assertEqual(self.instance.measurement_type_code, test_value)
    
    def test_water_column_height_property(self):
        """
        Test water_column_height property
        """
        test_value = float(82.38272141564141)
        self.instance.water_column_height = test_value
        self.assertEqual(self.instance.water_column_height, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyDartMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
