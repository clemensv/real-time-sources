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
            inDomain='xcihjqghqptlisbmixpq',
            price=float(38.93364678557002),
            currency='bpbnfooclxnmatlmbaru',
            unitName='tgvpxxofcbrdfipfgmaq',
            resolution='yodxrcporakoedxivkzf',
            documentType='lnoweeskkhqkgupiapjn'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'xcihjqghqptlisbmixpq'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(38.93364678557002)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'bpbnfooclxnmatlmbaru'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'tgvpxxofcbrdfipfgmaq'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'yodxrcporakoedxivkzf'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'lnoweeskkhqkgupiapjn'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DayAheadPrices.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
