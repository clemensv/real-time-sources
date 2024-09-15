"""
Test case for FareProducts
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.fareproducts import FareProducts

class Test_FareProducts(unittest.TestCase):
    """
    Test case for FareProducts
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareProducts.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareProducts for testing
        """
        instance = FareProducts(
            fareProductId='oprpyrrjregyzzjaeoec',
            fareProductName='julwywixcyiymxxanbut',
            fareProductDesc='kedhverjwpqxtcmtggpa',
            fareProductUrl='xtunmzodhyeghaxfrlma'
        )
        return instance

    
    def test_fareProductId_property(self):
        """
        Test fareProductId property
        """
        test_value = 'oprpyrrjregyzzjaeoec'
        self.instance.fareProductId = test_value
        self.assertEqual(self.instance.fareProductId, test_value)
    
    def test_fareProductName_property(self):
        """
        Test fareProductName property
        """
        test_value = 'julwywixcyiymxxanbut'
        self.instance.fareProductName = test_value
        self.assertEqual(self.instance.fareProductName, test_value)
    
    def test_fareProductDesc_property(self):
        """
        Test fareProductDesc property
        """
        test_value = 'kedhverjwpqxtcmtggpa'
        self.instance.fareProductDesc = test_value
        self.assertEqual(self.instance.fareProductDesc, test_value)
    
    def test_fareProductUrl_property(self):
        """
        Test fareProductUrl property
        """
        test_value = 'xtunmzodhyeghaxfrlma'
        self.instance.fareProductUrl = test_value
        self.assertEqual(self.instance.fareProductUrl, test_value)
    
