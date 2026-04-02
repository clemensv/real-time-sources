"""
Test case for Networks
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.networks import Networks


class Test_Networks(unittest.TestCase):
    """
    Test case for Networks
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Networks.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Networks for testing
        """
        instance = Networks(
            networkId='nkdmaosnhzpnnmsikfpi',
            networkName='eygcydwzbbfaprxvcrry',
            networkDesc='tzvcckyiqgqrrkgtyfrj',
            networkUrl='nvzcqtixsicfugzthbca'
        )
        return instance

    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'nkdmaosnhzpnnmsikfpi'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_networkName_property(self):
        """
        Test networkName property
        """
        test_value = 'eygcydwzbbfaprxvcrry'
        self.instance.networkName = test_value
        self.assertEqual(self.instance.networkName, test_value)
    
    def test_networkDesc_property(self):
        """
        Test networkDesc property
        """
        test_value = 'tzvcckyiqgqrrkgtyfrj'
        self.instance.networkDesc = test_value
        self.assertEqual(self.instance.networkDesc, test_value)
    
    def test_networkUrl_property(self):
        """
        Test networkUrl property
        """
        test_value = 'nvzcqtixsicfugzthbca'
        self.instance.networkUrl = test_value
        self.assertEqual(self.instance.networkUrl, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Networks.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
