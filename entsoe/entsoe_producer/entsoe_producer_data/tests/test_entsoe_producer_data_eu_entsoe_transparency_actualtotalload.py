"""
Test case for ActualTotalLoad
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.actualtotalload import ActualTotalLoad


class Test_ActualTotalLoad(unittest.TestCase):
    """
    Test case for ActualTotalLoad
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ActualTotalLoad.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ActualTotalLoad for testing
        """
        instance = ActualTotalLoad(
            inDomain='mdpqqvvuhzxgqitzobrc',
            quantity=float(54.80003675682569),
            resolution='zeircezzpqcvlwoqatsl',
            outDomain='acwlrfucubnnkgsguelo',
            documentType='bmbsnpozbcmlultiksnd'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'mdpqqvvuhzxgqitzobrc'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(54.80003675682569)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'zeircezzpqcvlwoqatsl'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_outDomain_property(self):
        """
        Test outDomain property
        """
        test_value = 'acwlrfucubnnkgsguelo'
        self.instance.outDomain = test_value
        self.assertEqual(self.instance.outDomain, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'bmbsnpozbcmlultiksnd'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ActualTotalLoad.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
