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
            locationGroupStoreId='wyeiikyvtvolueiigluf',
            locationGroupId='uenccfskzpmsvjrpblml',
            storeId='pxieqvqeoyybqzjrkmqn'
        )
        return instance

    
    def test_locationGroupStoreId_property(self):
        """
        Test locationGroupStoreId property
        """
        test_value = 'wyeiikyvtvolueiigluf'
        self.instance.locationGroupStoreId = test_value
        self.assertEqual(self.instance.locationGroupStoreId, test_value)
    
    def test_locationGroupId_property(self):
        """
        Test locationGroupId property
        """
        test_value = 'uenccfskzpmsvjrpblml'
        self.instance.locationGroupId = test_value
        self.assertEqual(self.instance.locationGroupId, test_value)
    
    def test_storeId_property(self):
        """
        Test storeId property
        """
        test_value = 'pxieqvqeoyybqzjrkmqn'
        self.instance.storeId = test_value
        self.assertEqual(self.instance.storeId, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LocationGroupStores.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
