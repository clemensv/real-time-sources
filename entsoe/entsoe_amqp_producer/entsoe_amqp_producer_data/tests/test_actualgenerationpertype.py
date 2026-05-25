"""
Test case for ActualGenerationPerType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_amqp_producer_data.eu.entsoe.transparency.actualgenerationpertype import ActualGenerationPerType


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
            inDomain='mnqanwwuzwcpljgsfjep',
            psrType='cbcfovasfmemlaclwvff',
            quantity=float(4.352329393202714),
            resolution='lzbhaumqgmdthtjtinfn',
            businessType='yoyhiqxixatgwyczhrfl',
            documentType='ecjsubenwcgzfmlywqox',
            unitName='xwcyaiziwybndtynmmfj'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'mnqanwwuzwcpljgsfjep'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_psrType_property(self):
        """
        Test psrType property
        """
        test_value = 'cbcfovasfmemlaclwvff'
        self.instance.psrType = test_value
        self.assertEqual(self.instance.psrType, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(4.352329393202714)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'lzbhaumqgmdthtjtinfn'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_businessType_property(self):
        """
        Test businessType property
        """
        test_value = 'yoyhiqxixatgwyczhrfl'
        self.instance.businessType = test_value
        self.assertEqual(self.instance.businessType, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'ecjsubenwcgzfmlywqox'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'xwcyaiziwybndtynmmfj'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ActualGenerationPerType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ActualGenerationPerType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

