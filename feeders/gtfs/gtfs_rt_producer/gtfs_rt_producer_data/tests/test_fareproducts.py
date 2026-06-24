"""
Test case for FareProducts
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.fareproducts import FareProducts


class Test_FareProducts(unittest.TestCase):
    """
    Test case for FareProducts
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareProducts.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareProducts for testing
        """
        instance = FareProducts(
            fareProductId='ggrlvortdlbobrlqseqn',
            fareProductName='mouxxezlibxbyvumqjsu',
            fareProductDesc='phutaagnbwoarlkweewp',
            fareProductUrl='qoghhgpdgjpzsuaskijm'
        )
        return instance

    
    def test_fareProductId_property(self):
        """
        Test fareProductId property
        """
        test_value = 'ggrlvortdlbobrlqseqn'
        self.instance.fareProductId = test_value
        self.assertEqual(self.instance.fareProductId, test_value)
    
    def test_fareProductName_property(self):
        """
        Test fareProductName property
        """
        test_value = 'mouxxezlibxbyvumqjsu'
        self.instance.fareProductName = test_value
        self.assertEqual(self.instance.fareProductName, test_value)
    
    def test_fareProductDesc_property(self):
        """
        Test fareProductDesc property
        """
        test_value = 'phutaagnbwoarlkweewp'
        self.instance.fareProductDesc = test_value
        self.assertEqual(self.instance.fareProductDesc, test_value)
    
    def test_fareProductUrl_property(self):
        """
        Test fareProductUrl property
        """
        test_value = 'qoghhgpdgjpzsuaskijm'
        self.instance.fareProductUrl = test_value
        self.assertEqual(self.instance.fareProductUrl, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FareProducts.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FareProducts.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

