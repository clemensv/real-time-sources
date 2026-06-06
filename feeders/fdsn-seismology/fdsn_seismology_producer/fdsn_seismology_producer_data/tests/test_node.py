"""
Test case for Node
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fdsn_seismology_producer_data.org.fdsn.event.node import Node


class Test_Node(unittest.TestCase):
    """
    Test case for Node
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Node.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Node for testing
        """
        instance = Node(
            node_id='ydovuszwjmkbiwbycgcl',
            name='azqwgbbfbjwbyulfhgif',
            base_url='ysroydndghsgjtqhlnwg',
            coverage='ikmbhyazmqhushsdtfqy',
            country='rmvzgsovgueevyzknads'
        )
        return instance

    
    def test_node_id_property(self):
        """
        Test node_id property
        """
        test_value = 'ydovuszwjmkbiwbycgcl'
        self.instance.node_id = test_value
        self.assertEqual(self.instance.node_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'azqwgbbfbjwbyulfhgif'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'ysroydndghsgjtqhlnwg'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_coverage_property(self):
        """
        Test coverage property
        """
        test_value = 'ikmbhyazmqhushsdtfqy'
        self.instance.coverage = test_value
        self.assertEqual(self.instance.coverage, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'rmvzgsovgueevyzknads'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Node.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Node.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

