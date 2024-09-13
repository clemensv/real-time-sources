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
            fareId='fnjdiiwqpphtwzcpcjdo',
            price=float(0.4086957264728186),
            currencyType='javmtygkukvmbukkdblc',
            paymentMethod=int(73),
            transfers=int(39),
            agencyId='hkueediqoxpxixtftohq',
            transferDuration=int(60)
        )
        return instance

    
    def test_fareId_property(self):
        """
        Test fareId property
        """
        test_value = 'fnjdiiwqpphtwzcpcjdo'
        self.instance.fareId = test_value
        self.assertEqual(self.instance.fareId, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(0.4086957264728186)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_currencyType_property(self):
        """
        Test currencyType property
        """
        test_value = 'javmtygkukvmbukkdblc'
        self.instance.currencyType = test_value
        self.assertEqual(self.instance.currencyType, test_value)
    
    def test_paymentMethod_property(self):
        """
        Test paymentMethod property
        """
        test_value = int(73)
        self.instance.paymentMethod = test_value
        self.assertEqual(self.instance.paymentMethod, test_value)
    
    def test_transfers_property(self):
        """
        Test transfers property
        """
        test_value = int(39)
        self.instance.transfers = test_value
        self.assertEqual(self.instance.transfers, test_value)
    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'hkueediqoxpxixtftohq'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_transferDuration_property(self):
        """
        Test transferDuration property
        """
        test_value = int(60)
        self.instance.transferDuration = test_value
        self.assertEqual(self.instance.transferDuration, test_value)
    
