"""
Test case for InstalledGenerationCapacityPerType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.installedgenerationcapacitypertype import InstalledGenerationCapacityPerType


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
            inDomain='mncxzvtxejesdvxmaddx',
            psrType='elrmfrgtfmetaqtmkkso',
            quantity=float(71.25102197882848),
            resolution='bspcejcjscyuhnsghgvy',
            businessType='vtwnmhfzpvqqnsflpixe',
            documentType='pyugmncqkzvnfojsxgfo',
            unitName='kdpowbrvctbrwrswhnxm'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'mncxzvtxejesdvxmaddx'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_psrType_property(self):
        """
        Test psrType property
        """
        test_value = 'elrmfrgtfmetaqtmkkso'
        self.instance.psrType = test_value
        self.assertEqual(self.instance.psrType, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(71.25102197882848)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'bspcejcjscyuhnsghgvy'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_businessType_property(self):
        """
        Test businessType property
        """
        test_value = 'vtwnmhfzpvqqnsflpixe'
        self.instance.businessType = test_value
        self.assertEqual(self.instance.businessType, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'pyugmncqkzvnfojsxgfo'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'kdpowbrvctbrwrswhnxm'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = InstalledGenerationCapacityPerType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
