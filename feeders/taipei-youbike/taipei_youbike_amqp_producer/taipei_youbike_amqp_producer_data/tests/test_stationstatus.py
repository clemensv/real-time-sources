"""
Test case for StationStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from taipei_youbike_amqp_producer_data.tw.youbike.stationstatus import StationStatus
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
            station_id='vpnesgcchfnmnksostsn',
            num_bikes_available=int(7),
            num_bikes_yb1=int(90),
            num_bikes_yb2=int(31),
            num_ebikes_available=int(56),
            num_empty_docks=int(49),
            num_forbidden_docks=int(11),
            availability_level=int(35),
            service_status=int(87),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            snapshot_time=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vpnesgcchfnmnksostsn'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_num_bikes_available_property(self):
        """
        Test num_bikes_available property
        """
        test_value = int(7)
        self.instance.num_bikes_available = test_value
        self.assertEqual(self.instance.num_bikes_available, test_value)
    
    def test_num_bikes_yb1_property(self):
        """
        Test num_bikes_yb1 property
        """
        test_value = int(90)
        self.instance.num_bikes_yb1 = test_value
        self.assertEqual(self.instance.num_bikes_yb1, test_value)
    
    def test_num_bikes_yb2_property(self):
        """
        Test num_bikes_yb2 property
        """
        test_value = int(31)
        self.instance.num_bikes_yb2 = test_value
        self.assertEqual(self.instance.num_bikes_yb2, test_value)
    
    def test_num_ebikes_available_property(self):
        """
        Test num_ebikes_available property
        """
        test_value = int(56)
        self.instance.num_ebikes_available = test_value
        self.assertEqual(self.instance.num_ebikes_available, test_value)
    
    def test_num_empty_docks_property(self):
        """
        Test num_empty_docks property
        """
        test_value = int(49)
        self.instance.num_empty_docks = test_value
        self.assertEqual(self.instance.num_empty_docks, test_value)
    
    def test_num_forbidden_docks_property(self):
        """
        Test num_forbidden_docks property
        """
        test_value = int(11)
        self.instance.num_forbidden_docks = test_value
        self.assertEqual(self.instance.num_forbidden_docks, test_value)
    
    def test_availability_level_property(self):
        """
        Test availability_level property
        """
        test_value = int(35)
        self.instance.availability_level = test_value
        self.assertEqual(self.instance.availability_level, test_value)
    
    def test_service_status_property(self):
        """
        Test service_status property
        """
        test_value = int(87)
        self.instance.service_status = test_value
        self.assertEqual(self.instance.service_status, test_value)
    
    def test_updated_at_property(self):
        """
        Test updated_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated_at = test_value
        self.assertEqual(self.instance.updated_at, test_value)
    
    def test_snapshot_time_property(self):
        """
        Test snapshot_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.snapshot_time = test_value
        self.assertEqual(self.instance.snapshot_time, test_value)
    
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

