"""
Test case for RadarProductCatalog
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_amqp_producer_data.radarproductcatalog import RadarProductCatalog


class Test_RadarProductCatalog(unittest.TestCase):
    """
    Test case for RadarProductCatalog
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RadarProductCatalog.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RadarProductCatalog for testing
        """
        instance = RadarProductCatalog(
            product='fudnfjlwaqusgchygpak',
            file_url='ziybhjytrexnvqxkczjt',
            description='rdgtfrvggqkevppsjpgl',
            state='mbrifyuiknhufjmbxoug',
            kind='bryijbrrfafnevtizwer'
        )
        return instance

    
    def test_product_property(self):
        """
        Test product property
        """
        test_value = 'fudnfjlwaqusgchygpak'
        self.instance.product = test_value
        self.assertEqual(self.instance.product, test_value)
    
    def test_file_url_property(self):
        """
        Test file_url property
        """
        test_value = 'ziybhjytrexnvqxkczjt'
        self.instance.file_url = test_value
        self.assertEqual(self.instance.file_url, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'rdgtfrvggqkevppsjpgl'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'mbrifyuiknhufjmbxoug'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_kind_property(self):
        """
        Test kind property
        """
        test_value = 'bryijbrrfafnevtizwer'
        self.instance.kind = test_value
        self.assertEqual(self.instance.kind, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RadarProductCatalog.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RadarProductCatalog.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

