"""
Test case for RouteNetworks
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.routenetworks import RouteNetworks


class Test_RouteNetworks(unittest.TestCase):
    """
    Test case for RouteNetworks
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RouteNetworks.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RouteNetworks for testing
        """
        instance = RouteNetworks(
            routeNetworkId='hbcxhioxrrlwddoipeym',
            routeId='qbackyvinglitqvwuniw',
            networkId='woyodfavwcpqpvuvpifk'
        )
        return instance

    
    def test_routeNetworkId_property(self):
        """
        Test routeNetworkId property
        """
        test_value = 'hbcxhioxrrlwddoipeym'
        self.instance.routeNetworkId = test_value
        self.assertEqual(self.instance.routeNetworkId, test_value)
    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'qbackyvinglitqvwuniw'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'woyodfavwcpqpvuvpifk'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RouteNetworks.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RouteNetworks.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

