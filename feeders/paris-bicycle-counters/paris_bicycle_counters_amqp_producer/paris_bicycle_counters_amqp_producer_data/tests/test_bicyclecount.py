"""
Test case for BicycleCount
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from paris_bicycle_counters_amqp_producer_data.bicyclecount import BicycleCount
import datetime


class Test_BicycleCount(unittest.TestCase):
    """
    Test case for BicycleCount
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BicycleCount.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BicycleCount for testing
        """
        instance = BicycleCount(
            counter_id='kabqkeavajkhydlcsvhi',
            counter_name='qblopoyknrbddiitwzfm',
            count=int(69),
            date=datetime.datetime.now(datetime.timezone.utc),
            longitude=float(30.126790350020038),
            latitude=float(28.982268438969893),
            ce_id='kizxxfzqbnuxffxqqekc'
        )
        return instance

    
    def test_counter_id_property(self):
        """
        Test counter_id property
        """
        test_value = 'kabqkeavajkhydlcsvhi'
        self.instance.counter_id = test_value
        self.assertEqual(self.instance.counter_id, test_value)
    
    def test_counter_name_property(self):
        """
        Test counter_name property
        """
        test_value = 'qblopoyknrbddiitwzfm'
        self.instance.counter_name = test_value
        self.assertEqual(self.instance.counter_name, test_value)
    
    def test_count_property(self):
        """
        Test count property
        """
        test_value = int(69)
        self.instance.count = test_value
        self.assertEqual(self.instance.count, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(30.126790350020038)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(28.982268438969893)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_ce_id_property(self):
        """
        Test ce_id property
        """
        test_value = 'kizxxfzqbnuxffxqqekc'
        self.instance.ce_id = test_value
        self.assertEqual(self.instance.ce_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BicycleCount.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BicycleCount.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

