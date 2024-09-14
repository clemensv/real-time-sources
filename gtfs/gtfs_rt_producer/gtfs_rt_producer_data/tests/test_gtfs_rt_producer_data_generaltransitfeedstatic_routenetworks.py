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
            routeNetworkId='bcpuioafolstzynwreio',
            routeId='xwcfxzncloxnpirjdsmn',
            networkId='bqmzamdrjcrcxkqwpcdb'
        )
        return instance

    
    def test_routeNetworkId_property(self):
        """
        Test routeNetworkId property
        """
        test_value = 'bcpuioafolstzynwreio'
        self.instance.routeNetworkId = test_value
        self.assertEqual(self.instance.routeNetworkId, test_value)
    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'xwcfxzncloxnpirjdsmn'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'bqmzamdrjcrcxkqwpcdb'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
