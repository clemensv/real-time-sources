"""
Test case for ForecastModelCatalog
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.forecastmodelcatalog import ForecastModelCatalog


class Test_ForecastModelCatalog(unittest.TestCase):
    """
    Test case for ForecastModelCatalog
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ForecastModelCatalog.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ForecastModelCatalog for testing
        """
        instance = ForecastModelCatalog(
            model='koodueewyoxftfoswyev',
            base_path='kwlqpgjeepzqvrdmaqkn',
            description='miahjgnqrzhscllycrwm',
            file_path='oyijmlemkersiodgnvte'
        )
        return instance

    
    def test_model_property(self):
        """
        Test model property
        """
        test_value = 'koodueewyoxftfoswyev'
        self.instance.model = test_value
        self.assertEqual(self.instance.model, test_value)
    
    def test_base_path_property(self):
        """
        Test base_path property
        """
        test_value = 'kwlqpgjeepzqvrdmaqkn'
        self.instance.base_path = test_value
        self.assertEqual(self.instance.base_path, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'miahjgnqrzhscllycrwm'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_file_path_property(self):
        """
        Test file_path property
        """
        test_value = 'oyijmlemkersiodgnvte'
        self.instance.file_path = test_value
        self.assertEqual(self.instance.file_path, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ForecastModelCatalog.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ForecastModelCatalog.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

