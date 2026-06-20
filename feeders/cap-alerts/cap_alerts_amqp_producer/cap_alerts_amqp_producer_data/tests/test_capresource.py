"""
Test case for CapResource
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.capresource import CapResource


class Test_CapResource(unittest.TestCase):
    """
    Test case for CapResource
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CapResource.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CapResource for testing
        """
        instance = CapResource(
            resource_desc='qkstvrwvvmvoxklmjnkf',
            mime_type='qwvgckshsjlwmgsuzlct',
            size=int(90),
            uri='ilojusrtwduxicyypsxj',
            deref_uri=b"test_bytes",
            digest='tmwuwsvokhhcernrqwgk'
        )
        return instance

    
    def test_resource_desc_property(self):
        """
        Test resource_desc property
        """
        test_value = 'qkstvrwvvmvoxklmjnkf'
        self.instance.resource_desc = test_value
        self.assertEqual(self.instance.resource_desc, test_value)
    
    def test_mime_type_property(self):
        """
        Test mime_type property
        """
        test_value = 'qwvgckshsjlwmgsuzlct'
        self.instance.mime_type = test_value
        self.assertEqual(self.instance.mime_type, test_value)
    
    def test_size_property(self):
        """
        Test size property
        """
        test_value = int(90)
        self.instance.size = test_value
        self.assertEqual(self.instance.size, test_value)
    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'ilojusrtwduxicyypsxj'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_deref_uri_property(self):
        """
        Test deref_uri property
        """
        test_value = b"test_bytes"
        self.instance.deref_uri = test_value
        self.assertEqual(self.instance.deref_uri, test_value)
    
    def test_digest_property(self):
        """
        Test digest property
        """
        test_value = 'tmwuwsvokhhcernrqwgk'
        self.instance.digest = test_value
        self.assertEqual(self.instance.digest, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CapResource.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CapResource.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

