"""
Test case for FareAttributes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.fareattributes import FareAttributes


class Test_FareAttributes(unittest.TestCase):
    """
    Test case for FareAttributes
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareAttributes.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareAttributes for testing
        """
        instance = FareAttributes(
            fareId='tsxwotpxugdqrkidekxt',
            price=float(60.026540701875206),
            currencyType='cmndyqofwryiekfztugd',
            paymentMethod=int(12),
            transfers=int(90),
            agencyId='iwteemjyryqfihvdszua',
            transferDuration=int(97)
        )
        return instance

    
    def test_fareId_property(self):
        """
        Test fareId property
        """
        test_value = 'tsxwotpxugdqrkidekxt'
        self.instance.fareId = test_value
        self.assertEqual(self.instance.fareId, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(60.026540701875206)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_currencyType_property(self):
        """
        Test currencyType property
        """
        test_value = 'cmndyqofwryiekfztugd'
        self.instance.currencyType = test_value
        self.assertEqual(self.instance.currencyType, test_value)
    
    def test_paymentMethod_property(self):
        """
        Test paymentMethod property
        """
        test_value = int(12)
        self.instance.paymentMethod = test_value
        self.assertEqual(self.instance.paymentMethod, test_value)
    
    def test_transfers_property(self):
        """
        Test transfers property
        """
        test_value = int(90)
        self.instance.transfers = test_value
        self.assertEqual(self.instance.transfers, test_value)
    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'iwteemjyryqfihvdszua'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_transferDuration_property(self):
        """
        Test transferDuration property
        """
        test_value = int(97)
        self.instance.transferDuration = test_value
        self.assertEqual(self.instance.transferDuration, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FareAttributes.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
