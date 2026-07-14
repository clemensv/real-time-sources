"""
Test case for StationStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tfl_cycles_mqtt_producer_data.stationstatus import StationStatus
import datetime


class Test_StationStatus(unittest.TestCase):
    """
    Test case for StationStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationStatus for testing
        """
        instance = StationStatus(
            station_id='vzeywyxgrqirusqspkrq',
            num_bikes_available=int(16),
            num_standard_bikes_available=int(51),
            num_ebikes_available=int(0),
            num_empty_docks=int(88),
            num_docks=int(39),
            is_installed=False,
            is_locked=False,
            modified=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vzeywyxgrqirusqspkrq'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_num_bikes_available_property(self):
        """
        Test num_bikes_available property
        """
        test_value = int(16)
        self.instance.num_bikes_available = test_value
        self.assertEqual(self.instance.num_bikes_available, test_value)
    
    def test_num_standard_bikes_available_property(self):
        """
        Test num_standard_bikes_available property
        """
        test_value = int(51)
        self.instance.num_standard_bikes_available = test_value
        self.assertEqual(self.instance.num_standard_bikes_available, test_value)
    
    def test_num_ebikes_available_property(self):
        """
        Test num_ebikes_available property
        """
        test_value = int(0)
        self.instance.num_ebikes_available = test_value
        self.assertEqual(self.instance.num_ebikes_available, test_value)
    
    def test_num_empty_docks_property(self):
        """
        Test num_empty_docks property
        """
        test_value = int(88)
        self.instance.num_empty_docks = test_value
        self.assertEqual(self.instance.num_empty_docks, test_value)
    
    def test_num_docks_property(self):
        """
        Test num_docks property
        """
        test_value = int(39)
        self.instance.num_docks = test_value
        self.assertEqual(self.instance.num_docks, test_value)
    
    def test_is_installed_property(self):
        """
        Test is_installed property
        """
        test_value = False
        self.instance.is_installed = test_value
        self.assertEqual(self.instance.is_installed, test_value)
    
    def test_is_locked_property(self):
        """
        Test is_locked property
        """
        test_value = False
        self.instance.is_locked = test_value
        self.assertEqual(self.instance.is_locked, test_value)
    
    def test_modified_property(self):
        """
        Test modified property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.modified = test_value
        self.assertEqual(self.instance.modified, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationStatus.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

