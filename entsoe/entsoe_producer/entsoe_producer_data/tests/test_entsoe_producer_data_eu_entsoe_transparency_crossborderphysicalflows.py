"""
Test case for CrossBorderPhysicalFlows
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.crossborderphysicalflows import CrossBorderPhysicalFlows


class Test_CrossBorderPhysicalFlows(unittest.TestCase):
    """
    Test case for CrossBorderPhysicalFlows
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CrossBorderPhysicalFlows.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CrossBorderPhysicalFlows for testing
        """
        instance = CrossBorderPhysicalFlows(
            inDomain='shjvjnhlyfqigtjaysqx',
            outDomain='icsvoprctphcgvybhqqv',
            quantity=float(28.924963380761337),
            resolution='uyyvpgcxopwbfwpynkyc',
            documentType='moncoeqwxgkgnotgugyb',
            unitName='calaoagzjrsghnwyzkhj'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'shjvjnhlyfqigtjaysqx'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_outDomain_property(self):
        """
        Test outDomain property
        """
        test_value = 'icsvoprctphcgvybhqqv'
        self.instance.outDomain = test_value
        self.assertEqual(self.instance.outDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(28.924963380761337)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'uyyvpgcxopwbfwpynkyc'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'moncoeqwxgkgnotgugyb'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'calaoagzjrsghnwyzkhj'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CrossBorderPhysicalFlows.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
