"""
Test case for GenerationForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.generationforecast import GenerationForecast


class Test_GenerationForecast(unittest.TestCase):
    """
    Test case for GenerationForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GenerationForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GenerationForecast for testing
        """
        instance = GenerationForecast(
            inDomain='qhvvnltcgpsonaoevhul',
            quantity=float(17.35590012859729),
            resolution='ypcdsxcwldvtnkxyarub',
            documentType='xeggaxjomqqzfpelodfb',
            unitName='aornvvygibdbwvmfduqh'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'qhvvnltcgpsonaoevhul'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(17.35590012859729)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'ypcdsxcwldvtnkxyarub'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'xeggaxjomqqzfpelodfb'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'aornvvygibdbwvmfduqh'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GenerationForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GenerationForecast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

