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
            inDomain='vysjhzegjeusydracpdj',
            quantity=float(58.956794105709676),
            resolution='llxxcytcykdtpsujjbjc',
            documentType='grjbqixwojgqjqhatelp',
            unitName='imtvggrtancrdlbqlium'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'vysjhzegjeusydracpdj'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(58.956794105709676)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'llxxcytcykdtpsujjbjc'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'grjbqixwojgqjqhatelp'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'imtvggrtancrdlbqlium'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ActualGeneration.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
