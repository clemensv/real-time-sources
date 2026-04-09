"""
Test case for Region
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_pollenflug_producer_data.region import Region


class Test_Region(unittest.TestCase):
    """
    Test case for Region
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Region.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Region for testing
        """
        instance = Region(
            region_id=int(77),
            region_name='bscgnesbldglbpeahjfb',
            partregion_id=int(7),
            partregion_name='bgofujtqsiyveongrnlk'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(77)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_region_name_property(self):
        """
        Test region_name property
        """
        test_value = 'bscgnesbldglbpeahjfb'
        self.instance.region_name = test_value
        self.assertEqual(self.instance.region_name, test_value)
    
    def test_partregion_id_property(self):
        """
        Test partregion_id property
        """
        test_value = int(7)
        self.instance.partregion_id = test_value
        self.assertEqual(self.instance.partregion_id, test_value)
    
    def test_partregion_name_property(self):
        """
        Test partregion_name property
        """
        test_value = 'bgofujtqsiyveongrnlk'
        self.instance.partregion_name = test_value
        self.assertEqual(self.instance.partregion_name, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Region.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Region.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

