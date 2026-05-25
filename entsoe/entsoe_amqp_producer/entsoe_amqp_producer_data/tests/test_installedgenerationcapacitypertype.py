"""
Test case for InstalledGenerationCapacityPerType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_amqp_producer_data.eu.entsoe.transparency.installedgenerationcapacitypertype import InstalledGenerationCapacityPerType


class Test_InstalledGenerationCapacityPerType(unittest.TestCase):
    """
    Test case for InstalledGenerationCapacityPerType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_InstalledGenerationCapacityPerType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of InstalledGenerationCapacityPerType for testing
        """
        instance = InstalledGenerationCapacityPerType(
            inDomain='faatpyakkguachhmpbnn',
            psrType='snubtdimzutekghsfxfi',
            quantity=float(16.670904099117834),
            resolution='gnphsgruylgmrsocgolt',
            businessType='bdcytzvzvgauhtlgvgye',
            documentType='ylhgogtesctxcbxccocu',
            unitName='uacfkkvesekttvfqwteu'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'faatpyakkguachhmpbnn'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_psrType_property(self):
        """
        Test psrType property
        """
        test_value = 'snubtdimzutekghsfxfi'
        self.instance.psrType = test_value
        self.assertEqual(self.instance.psrType, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(16.670904099117834)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'gnphsgruylgmrsocgolt'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_businessType_property(self):
        """
        Test businessType property
        """
        test_value = 'bdcytzvzvgauhtlgvgye'
        self.instance.businessType = test_value
        self.assertEqual(self.instance.businessType, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'ylhgogtesctxcbxccocu'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'uacfkkvesekttvfqwteu'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = InstalledGenerationCapacityPerType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = InstalledGenerationCapacityPerType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

