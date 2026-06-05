"""
Test case for FareAttributes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.fareattributes import FareAttributes


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
            fareId='bxidzodpwgglgulwmwlg',
            price=float(36.37192633423163),
            currencyType='hcivzdnheioeakehuhjj',
            paymentMethod=int(90),
            transfers=int(0),
            agencyId='acaadybcyjgrkenbabyc',
            transferDuration=int(23)
        )
        return instance

    
    def test_fareId_property(self):
        """
        Test fareId property
        """
        test_value = 'bxidzodpwgglgulwmwlg'
        self.instance.fareId = test_value
        self.assertEqual(self.instance.fareId, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(36.37192633423163)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_currencyType_property(self):
        """
        Test currencyType property
        """
        test_value = 'hcivzdnheioeakehuhjj'
        self.instance.currencyType = test_value
        self.assertEqual(self.instance.currencyType, test_value)
    
    def test_paymentMethod_property(self):
        """
        Test paymentMethod property
        """
        test_value = int(90)
        self.instance.paymentMethod = test_value
        self.assertEqual(self.instance.paymentMethod, test_value)
    
    def test_transfers_property(self):
        """
        Test transfers property
        """
        test_value = int(0)
        self.instance.transfers = test_value
        self.assertEqual(self.instance.transfers, test_value)
    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'acaadybcyjgrkenbabyc'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_transferDuration_property(self):
        """
        Test transferDuration property
        """
        test_value = int(23)
        self.instance.transferDuration = test_value
        self.assertEqual(self.instance.transferDuration, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FareAttributes.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FareAttributes.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

