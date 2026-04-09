"""
Test case for BicycleCount
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from paris_bicycle_counters_producer_data.bicyclecount import BicycleCount
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
            counter_id='sfbxcwzvccenohyrujrn',
            counter_name='zzyavjssbbvctapjpjpq',
            count=int(52),
            date=datetime.datetime.now(datetime.timezone.utc),
            longitude=float(0.6644814164313173),
            latitude=float(69.26355214965541)
        )
        return instance

    
    def test_counter_id_property(self):
        """
        Test counter_id property
        """
        test_value = 'sfbxcwzvccenohyrujrn'
        self.instance.counter_id = test_value
        self.assertEqual(self.instance.counter_id, test_value)
    
    def test_counter_name_property(self):
        """
        Test counter_name property
        """
        test_value = 'zzyavjssbbvctapjpjpq'
        self.instance.counter_name = test_value
        self.assertEqual(self.instance.counter_name, test_value)
    
    def test_count_property(self):
        """
        Test count property
        """
        test_value = int(52)
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
        test_value = float(0.6644814164313173)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(69.26355214965541)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
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

