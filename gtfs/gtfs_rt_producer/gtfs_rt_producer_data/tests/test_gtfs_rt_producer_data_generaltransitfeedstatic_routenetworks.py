"""
Test case for RouteNetworks
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.routenetworks import RouteNetworks


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
            routeNetworkId='lcbzhauwwnpqlsofvhos',
            routeId='jsfpcqslsyvjtuanaiua',
            networkId='ukwpnxqctnrhosksousb'
        )
        return instance

    
    def test_routeNetworkId_property(self):
        """
        Test routeNetworkId property
        """
        test_value = 'lcbzhauwwnpqlsofvhos'
        self.instance.routeNetworkId = test_value
        self.assertEqual(self.instance.routeNetworkId, test_value)
    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'jsfpcqslsyvjtuanaiua'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'ukwpnxqctnrhosksousb'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RouteNetworks.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
