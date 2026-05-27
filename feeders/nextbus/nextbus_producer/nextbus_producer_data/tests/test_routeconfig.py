"""
Test case for RouteConfig
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nextbus_producer_data.routeconfig import RouteConfig


class Test_RouteConfig(unittest.TestCase):
    """
    Test case for RouteConfig
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RouteConfig.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RouteConfig for testing
        """
        instance = RouteConfig(
            agency_id='ydxfihgvzxnqawpdqbah',
            route_tag='ewdeptxgfvybtekzocgg',
            stop_or_vehicle_id='qsfhrvbeszvvhlpeijut',
            event_type='lkeapxynlijkvpfuxcpn',
            route_config='cxprkjjnzeeswzqwyerm'
        )
        return instance

    
    def test_agency_id_property(self):
        """
        Test agency_id property
        """
        test_value = 'ydxfihgvzxnqawpdqbah'
        self.instance.agency_id = test_value
        self.assertEqual(self.instance.agency_id, test_value)
    
    def test_route_tag_property(self):
        """
        Test route_tag property
        """
        test_value = 'ewdeptxgfvybtekzocgg'
        self.instance.route_tag = test_value
        self.assertEqual(self.instance.route_tag, test_value)
    
    def test_stop_or_vehicle_id_property(self):
        """
        Test stop_or_vehicle_id property
        """
        test_value = 'qsfhrvbeszvvhlpeijut'
        self.instance.stop_or_vehicle_id = test_value
        self.assertEqual(self.instance.stop_or_vehicle_id, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'lkeapxynlijkvpfuxcpn'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_route_config_property(self):
        """
        Test route_config property
        """
        test_value = 'cxprkjjnzeeswzqwyerm'
        self.instance.route_config = test_value
        self.assertEqual(self.instance.route_config, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RouteConfig.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RouteConfig.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

