"""
Test case for ActualGeneration
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.actualgeneration import ActualGeneration


class Test_ActualGeneration(unittest.TestCase):
    """
    Test case for ActualGeneration
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ActualGeneration.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ActualGeneration for testing
        """
        instance = ActualGeneration(
            inDomain='xisztkhmuaibomvjysqv',
            quantity=float(28.85137800990386),
            resolution='mlklpssjxiwvzrswyjam',
            documentType='zbdwzccurbcttutjrflw',
            unitName='eyccsrpafwotvfnpkmev'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'xisztkhmuaibomvjysqv'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(28.85137800990386)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'mlklpssjxiwvzrswyjam'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'zbdwzccurbcttutjrflw'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'eyccsrpafwotvfnpkmev'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ActualGeneration.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ActualGeneration.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

