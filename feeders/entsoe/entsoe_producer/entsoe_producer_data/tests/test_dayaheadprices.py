"""
Test case for DayAheadPrices
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.dayaheadprices import DayAheadPrices


class Test_DayAheadPrices(unittest.TestCase):
    """
    Test case for DayAheadPrices
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DayAheadPrices.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DayAheadPrices for testing
        """
        instance = DayAheadPrices(
            inDomain='pndqrtzkcssnpvkjiqcx',
            price=float(8.210681195030233),
            currency='mtbffednnmihxszblpxf',
            unitName='umwqxgwdlktfkcdxnzls',
            resolution='dbgrzldxuoskfmrfdzeh',
            documentType='zmmxbufgxdgvjodaqljj'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'pndqrtzkcssnpvkjiqcx'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(8.210681195030233)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'mtbffednnmihxszblpxf'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'umwqxgwdlktfkcdxnzls'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'dbgrzldxuoskfmrfdzeh'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'zmmxbufgxdgvjodaqljj'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DayAheadPrices.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DayAheadPrices.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

