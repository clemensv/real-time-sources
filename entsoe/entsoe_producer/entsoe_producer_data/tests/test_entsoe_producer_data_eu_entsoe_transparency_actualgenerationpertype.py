"""
Test case for ActualGenerationPerType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.actualgenerationpertype import ActualGenerationPerType


class Test_ActualGenerationPerType(unittest.TestCase):
    """
    Test case for ActualGenerationPerType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ActualGenerationPerType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ActualGenerationPerType for testing
        """
        instance = ActualGenerationPerType(
            inDomain='paerujylbappzwmdmwti',
            psrType='jjmqtdnielivzhlwzgwz',
            quantity=float(58.16727386290582),
            resolution='ukofmqvrwgeqaynmwptt',
            businessType='wzrrkzvktfaqetgdubpl',
            documentType='jchmiwgscfbcpsgxkhxw',
            unitName='utrsmwjuxdtbezkaxtol'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'paerujylbappzwmdmwti'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_psrType_property(self):
        """
        Test psrType property
        """
        test_value = 'jjmqtdnielivzhlwzgwz'
        self.instance.psrType = test_value
        self.assertEqual(self.instance.psrType, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(58.16727386290582)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'ukofmqvrwgeqaynmwptt'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_businessType_property(self):
        """
        Test businessType property
        """
        test_value = 'wzrrkzvktfaqetgdubpl'
        self.instance.businessType = test_value
        self.assertEqual(self.instance.businessType, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'jchmiwgscfbcpsgxkhxw'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'utrsmwjuxdtbezkaxtol'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ActualGenerationPerType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
