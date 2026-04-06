"""
Test case for PriceComponent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.pricecomponent import PriceComponent
from ndl_netherlands_producer_data.typeenum import TypeEnum


class Test_PriceComponent(unittest.TestCase):
    """
    Test case for PriceComponent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PriceComponent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PriceComponent for testing
        """
        instance = PriceComponent(
            type=TypeEnum.ENERGY,
            price=float(45.29708044868488),
            vat=float(22.77127608695757),
            step_size=int(16)
        )
        return instance

    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = TypeEnum.ENERGY
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(45.29708044868488)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_vat_property(self):
        """
        Test vat property
        """
        test_value = float(22.77127608695757)
        self.instance.vat = test_value
        self.assertEqual(self.instance.vat, test_value)
    
    def test_step_size_property(self):
        """
        Test step_size property
        """
        test_value = int(16)
        self.instance.step_size = test_value
        self.assertEqual(self.instance.step_size, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PriceComponent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PriceComponent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

