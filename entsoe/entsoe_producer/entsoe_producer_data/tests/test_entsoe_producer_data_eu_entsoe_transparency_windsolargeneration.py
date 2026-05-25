"""
Test case for WindSolarGeneration
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.windsolargeneration import WindSolarGeneration


class Test_WindSolarGeneration(unittest.TestCase):
    """
    Test case for WindSolarGeneration
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WindSolarGeneration.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WindSolarGeneration for testing
        """
        instance = WindSolarGeneration(
            inDomain='jotxwtrsvetajuobraqc',
            psrType='xsymcguhbrhcpxfilcjg',
            quantity=float(43.6957886795872),
            resolution='gtadkdopmvctmdnjznjz',
            businessType='pmoaowzlpyfiskrhvhhg',
            documentType='lkowcnbozbouzoqapama',
            unitName='kinaggdtbvcyfbcwkxsp'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'jotxwtrsvetajuobraqc'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_psrType_property(self):
        """
        Test psrType property
        """
        test_value = 'xsymcguhbrhcpxfilcjg'
        self.instance.psrType = test_value
        self.assertEqual(self.instance.psrType, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(43.6957886795872)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'gtadkdopmvctmdnjznjz'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_businessType_property(self):
        """
        Test businessType property
        """
        test_value = 'pmoaowzlpyfiskrhvhhg'
        self.instance.businessType = test_value
        self.assertEqual(self.instance.businessType, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'lkowcnbozbouzoqapama'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'kinaggdtbvcyfbcwkxsp'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WindSolarGeneration.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
