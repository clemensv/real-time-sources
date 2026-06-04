"""
Test case for FreeBikeStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gbfs_bikeshare_mqtt_producer_data.freebikestatus import FreeBikeStatus


class Test_FreeBikeStatus(unittest.TestCase):
    """
    Test case for FreeBikeStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FreeBikeStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FreeBikeStatus for testing
        """
        instance = FreeBikeStatus(
            system_id='nizyhonqfzfgwmqcacaj',
            bike_id='maugsehmhgpjukxmhwuo',
            lat=float(76.15700590303715),
            lon=float(21.741703778495335),
            is_reserved=False,
            is_disabled=False,
            vehicle_type_id='cyfkekgnambxqafeccei',
            current_range_meters=float(64.29541459335123),
            last_reported=int(63)
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'nizyhonqfzfgwmqcacaj'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_bike_id_property(self):
        """
        Test bike_id property
        """
        test_value = 'maugsehmhgpjukxmhwuo'
        self.instance.bike_id = test_value
        self.assertEqual(self.instance.bike_id, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(76.15700590303715)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(21.741703778495335)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_is_reserved_property(self):
        """
        Test is_reserved property
        """
        test_value = False
        self.instance.is_reserved = test_value
        self.assertEqual(self.instance.is_reserved, test_value)
    
    def test_is_disabled_property(self):
        """
        Test is_disabled property
        """
        test_value = False
        self.instance.is_disabled = test_value
        self.assertEqual(self.instance.is_disabled, test_value)
    
    def test_vehicle_type_id_property(self):
        """
        Test vehicle_type_id property
        """
        test_value = 'cyfkekgnambxqafeccei'
        self.instance.vehicle_type_id = test_value
        self.assertEqual(self.instance.vehicle_type_id, test_value)
    
    def test_current_range_meters_property(self):
        """
        Test current_range_meters property
        """
        test_value = float(64.29541459335123)
        self.instance.current_range_meters = test_value
        self.assertEqual(self.instance.current_range_meters, test_value)
    
    def test_last_reported_property(self):
        """
        Test last_reported property
        """
        test_value = int(63)
        self.instance.last_reported = test_value
        self.assertEqual(self.instance.last_reported, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FreeBikeStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FreeBikeStatus.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

