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
            fareId='agbmnpiaoysimmubyuqu',
            price=float(50.39431017920468),
            currencyType='utvflopaurtoicqdcebk',
            paymentMethod=int(34),
            transfers=int(63),
            agencyId='mewwocpcktemydtubprd',
            transferDuration=int(46)
        )
        return instance

    
    def test_fareId_property(self):
        """
        Test fareId property
        """
        test_value = 'agbmnpiaoysimmubyuqu'
        self.instance.fareId = test_value
        self.assertEqual(self.instance.fareId, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(50.39431017920468)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_currencyType_property(self):
        """
        Test currencyType property
        """
        test_value = 'utvflopaurtoicqdcebk'
        self.instance.currencyType = test_value
        self.assertEqual(self.instance.currencyType, test_value)
    
    def test_paymentMethod_property(self):
        """
        Test paymentMethod property
        """
        test_value = int(34)
        self.instance.paymentMethod = test_value
        self.assertEqual(self.instance.paymentMethod, test_value)
    
    def test_transfers_property(self):
        """
        Test transfers property
        """
        test_value = int(63)
        self.instance.transfers = test_value
        self.assertEqual(self.instance.transfers, test_value)
    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'mewwocpcktemydtubprd'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_transferDuration_property(self):
        """
        Test transferDuration property
        """
        test_value = int(46)
        self.instance.transferDuration = test_value
        self.assertEqual(self.instance.transferDuration, test_value)
    
