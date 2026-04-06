"""
Test case for EvseStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.evsestatus import EvseStatus
from ndl_netherlands_producer_data.connectorsummary import ConnectorSummary
from typing import Any
from ndl_netherlands_producer_data.statusenum import StatusEnum
import datetime


class Test_EvseStatus(unittest.TestCase):
    """
    Test case for EvseStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EvseStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EvseStatus for testing
        """
        instance = EvseStatus(
            location_id='vodvjkkearcylptcvvmc',
            evse_uid='jybkenamktjyuulxuwiv',
            evse_id='fyuwwqwkcxxehbkbkobe',
            status=StatusEnum.AVAILABLE,
            capabilities=None,
            floor_level='cokhiidvmxhfxdcprhbh',
            latitude=float(83.89513744706177),
            longitude=float(83.69309957756292),
            physical_reference='wpfinqhnaollthafbqyj',
            parking_restrictions=None,
            connectors=[None, None, None],
            last_updated=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = 'vodvjkkearcylptcvvmc'
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_evse_uid_property(self):
        """
        Test evse_uid property
        """
        test_value = 'jybkenamktjyuulxuwiv'
        self.instance.evse_uid = test_value
        self.assertEqual(self.instance.evse_uid, test_value)
    
    def test_evse_id_property(self):
        """
        Test evse_id property
        """
        test_value = 'fyuwwqwkcxxehbkbkobe'
        self.instance.evse_id = test_value
        self.assertEqual(self.instance.evse_id, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = StatusEnum.AVAILABLE
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_capabilities_property(self):
        """
        Test capabilities property
        """
        test_value = None
        self.instance.capabilities = test_value
        self.assertEqual(self.instance.capabilities, test_value)
    
    def test_floor_level_property(self):
        """
        Test floor_level property
        """
        test_value = 'cokhiidvmxhfxdcprhbh'
        self.instance.floor_level = test_value
        self.assertEqual(self.instance.floor_level, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(83.89513744706177)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(83.69309957756292)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_physical_reference_property(self):
        """
        Test physical_reference property
        """
        test_value = 'wpfinqhnaollthafbqyj'
        self.instance.physical_reference = test_value
        self.assertEqual(self.instance.physical_reference, test_value)
    
    def test_parking_restrictions_property(self):
        """
        Test parking_restrictions property
        """
        test_value = None
        self.instance.parking_restrictions = test_value
        self.assertEqual(self.instance.parking_restrictions, test_value)
    
    def test_connectors_property(self):
        """
        Test connectors property
        """
        test_value = [None, None, None]
        self.instance.connectors = test_value
        self.assertEqual(self.instance.connectors, test_value)
    
    def test_last_updated_property(self):
        """
        Test last_updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.last_updated = test_value
        self.assertEqual(self.instance.last_updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EvseStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EvseStatus.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

