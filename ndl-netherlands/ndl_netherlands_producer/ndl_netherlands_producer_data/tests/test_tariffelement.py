"""
Test case for TariffElement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.tariffelement import TariffElement
from ndl_netherlands_producer_data.pricecomponent import PriceComponent
from ndl_netherlands_producer_data.tariffrestrictions import TariffRestrictions


class Test_TariffElement(unittest.TestCase):
    """
    Test case for TariffElement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TariffElement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TariffElement for testing
        """
        instance = TariffElement(
            price_components=[None, None, None, None, None],
            restrictions=None
        )
        return instance

    
    def test_price_components_property(self):
        """
        Test price_components property
        """
        test_value = [None, None, None, None, None]
        self.instance.price_components = test_value
        self.assertEqual(self.instance.price_components, test_value)
    
    def test_restrictions_property(self):
        """
        Test restrictions property
        """
        test_value = None
        self.instance.restrictions = test_value
        self.assertEqual(self.instance.restrictions, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TariffElement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TariffElement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

