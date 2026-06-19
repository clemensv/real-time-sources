"""
Test case for PSIReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from singapore_nea_producer_data.psireading import PSIReading
import datetime


class Test_PSIReading(unittest.TestCase):
    """
    Test case for PSIReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PSIReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PSIReading for testing
        """
        instance = PSIReading(
            region='hgjnthjprrjeyaefpsop',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            update_timestamp=datetime.datetime.now(datetime.timezone.utc),
            psi_twenty_four_hourly=int(60),
            o3_sub_index=int(56),
            pm10_sub_index=int(87),
            pm10_twenty_four_hourly=int(70),
            pm25_sub_index=int(70),
            pm25_twenty_four_hourly=int(38),
            co_sub_index=int(45),
            co_eight_hour_max=int(44),
            so2_sub_index=int(40),
            so2_twenty_four_hourly=int(7),
            no2_one_hour_max=int(91),
            o3_eight_hour_max=int(81)
        )
        return instance

    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'hgjnthjprrjeyaefpsop'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_update_timestamp_property(self):
        """
        Test update_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.update_timestamp = test_value
        self.assertEqual(self.instance.update_timestamp, test_value)
    
    def test_psi_twenty_four_hourly_property(self):
        """
        Test psi_twenty_four_hourly property
        """
        test_value = int(60)
        self.instance.psi_twenty_four_hourly = test_value
        self.assertEqual(self.instance.psi_twenty_four_hourly, test_value)
    
    def test_o3_sub_index_property(self):
        """
        Test o3_sub_index property
        """
        test_value = int(56)
        self.instance.o3_sub_index = test_value
        self.assertEqual(self.instance.o3_sub_index, test_value)
    
    def test_pm10_sub_index_property(self):
        """
        Test pm10_sub_index property
        """
        test_value = int(87)
        self.instance.pm10_sub_index = test_value
        self.assertEqual(self.instance.pm10_sub_index, test_value)
    
    def test_pm10_twenty_four_hourly_property(self):
        """
        Test pm10_twenty_four_hourly property
        """
        test_value = int(70)
        self.instance.pm10_twenty_four_hourly = test_value
        self.assertEqual(self.instance.pm10_twenty_four_hourly, test_value)
    
    def test_pm25_sub_index_property(self):
        """
        Test pm25_sub_index property
        """
        test_value = int(70)
        self.instance.pm25_sub_index = test_value
        self.assertEqual(self.instance.pm25_sub_index, test_value)
    
    def test_pm25_twenty_four_hourly_property(self):
        """
        Test pm25_twenty_four_hourly property
        """
        test_value = int(38)
        self.instance.pm25_twenty_four_hourly = test_value
        self.assertEqual(self.instance.pm25_twenty_four_hourly, test_value)
    
    def test_co_sub_index_property(self):
        """
        Test co_sub_index property
        """
        test_value = int(45)
        self.instance.co_sub_index = test_value
        self.assertEqual(self.instance.co_sub_index, test_value)
    
    def test_co_eight_hour_max_property(self):
        """
        Test co_eight_hour_max property
        """
        test_value = int(44)
        self.instance.co_eight_hour_max = test_value
        self.assertEqual(self.instance.co_eight_hour_max, test_value)
    
    def test_so2_sub_index_property(self):
        """
        Test so2_sub_index property
        """
        test_value = int(40)
        self.instance.so2_sub_index = test_value
        self.assertEqual(self.instance.so2_sub_index, test_value)
    
    def test_so2_twenty_four_hourly_property(self):
        """
        Test so2_twenty_four_hourly property
        """
        test_value = int(7)
        self.instance.so2_twenty_four_hourly = test_value
        self.assertEqual(self.instance.so2_twenty_four_hourly, test_value)
    
    def test_no2_one_hour_max_property(self):
        """
        Test no2_one_hour_max property
        """
        test_value = int(91)
        self.instance.no2_one_hour_max = test_value
        self.assertEqual(self.instance.no2_one_hour_max, test_value)
    
    def test_o3_eight_hour_max_property(self):
        """
        Test o3_eight_hour_max property
        """
        test_value = int(81)
        self.instance.o3_eight_hour_max = test_value
        self.assertEqual(self.instance.o3_eight_hour_max, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PSIReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PSIReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

