"""
Test case for Networks
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.networks import Networks


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
            networkId='wfshmanvbbqydlfvypfv',
            networkName='iujedjtfyowvvwqzgmtc',
            networkDesc='oiewknpqlvnodzrzhnyi',
            networkUrl='mllluuhxnnlialbzgmrv'
        )
        return instance

    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'wfshmanvbbqydlfvypfv'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_networkName_property(self):
        """
        Test networkName property
        """
        test_value = 'iujedjtfyowvvwqzgmtc'
        self.instance.networkName = test_value
        self.assertEqual(self.instance.networkName, test_value)
    
    def test_networkDesc_property(self):
        """
        Test networkDesc property
        """
        test_value = 'oiewknpqlvnodzrzhnyi'
        self.instance.networkDesc = test_value
        self.assertEqual(self.instance.networkDesc, test_value)
    
    def test_networkUrl_property(self):
        """
        Test networkUrl property
        """
        test_value = 'mllluuhxnnlialbzgmrv'
        self.instance.networkUrl = test_value
        self.assertEqual(self.instance.networkUrl, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Networks.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Networks.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

