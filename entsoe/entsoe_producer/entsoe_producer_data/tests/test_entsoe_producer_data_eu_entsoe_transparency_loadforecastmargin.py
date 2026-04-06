"""
Test case for LoadForecastMargin
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.loadforecastmargin import LoadForecastMargin


class Test_LoadForecastMargin(unittest.TestCase):
    """
    Test case for LoadForecastMargin
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LoadForecastMargin.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LoadForecastMargin for testing
        """
        instance = LoadForecastMargin(
            inDomain='angfzlqvkhmfjoqpopnq',
            quantity=float(32.33113321732842),
            resolution='ibxfwijireowgnjijuvj',
            documentType='ybttilvkbuaimoljlfgl',
            unitName='sitxpcehackbufmlxqsm'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'angfzlqvkhmfjoqpopnq'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(32.33113321732842)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'ibxfwijireowgnjijuvj'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'ybttilvkbuaimoljlfgl'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'sitxpcehackbufmlxqsm'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LoadForecastMargin.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
