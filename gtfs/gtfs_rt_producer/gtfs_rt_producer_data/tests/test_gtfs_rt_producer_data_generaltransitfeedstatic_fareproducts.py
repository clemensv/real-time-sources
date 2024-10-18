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
            fareProductId='ebrfsspviawuaaorwcob',
            fareProductName='zxfsawdobajjwzdvfbhn',
            fareProductDesc='lwgkvdkcqjhuqxgrxzpa',
            fareProductUrl='zjeqxuwntpyndjldgwvn'
        )
        return instance

    
    def test_fareProductId_property(self):
        """
        Test fareProductId property
        """
        test_value = 'ebrfsspviawuaaorwcob'
        self.instance.fareProductId = test_value
        self.assertEqual(self.instance.fareProductId, test_value)
    
    def test_fareProductName_property(self):
        """
        Test fareProductName property
        """
        test_value = 'zxfsawdobajjwzdvfbhn'
        self.instance.fareProductName = test_value
        self.assertEqual(self.instance.fareProductName, test_value)
    
    def test_fareProductDesc_property(self):
        """
        Test fareProductDesc property
        """
        test_value = 'lwgkvdkcqjhuqxgrxzpa'
        self.instance.fareProductDesc = test_value
        self.assertEqual(self.instance.fareProductDesc, test_value)
    
    def test_fareProductUrl_property(self):
        """
        Test fareProductUrl property
        """
        test_value = 'zjeqxuwntpyndjldgwvn'
        self.instance.fareProductUrl = test_value
        self.assertEqual(self.instance.fareProductUrl, test_value)
    
