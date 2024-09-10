"""
Test case for LocationGroupStores
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroupstores import LocationGroupStores

class Test_LocationGroupStores(unittest.TestCase):
    """
    Test case for LocationGroupStores
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LocationGroupStores.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LocationGroupStores for testing
        """
        instance = LocationGroupStores(
            locationGroupStoreId='apauvozwipxstmwujqkg',
            locationGroupId='jczkuhqodkqhnabuzquo',
            storeId='zmlurezbflvqvfpldpts'
        )
        return instance

    
    def test_locationGroupStoreId_property(self):
        """
        Test locationGroupStoreId property
        """
        test_value = 'apauvozwipxstmwujqkg'
        self.instance.locationGroupStoreId = test_value
        self.assertEqual(self.instance.locationGroupStoreId, test_value)
    
    def test_locationGroupId_property(self):
        """
        Test locationGroupId property
        """
        test_value = 'jczkuhqodkqhnabuzquo'
        self.instance.locationGroupId = test_value
        self.assertEqual(self.instance.locationGroupId, test_value)
    
    def test_storeId_property(self):
        """
        Test storeId property
        """
        test_value = 'zmlurezbflvqvfpldpts'
        self.instance.storeId = test_value
        self.assertEqual(self.instance.storeId, test_value)
    
