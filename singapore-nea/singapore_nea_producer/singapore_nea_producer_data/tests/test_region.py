"""
Test case for Region
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from singapore_nea_producer_data.region import Region


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
            region='uzoxyzdfkulxwerfmxpt',
            latitude=float(25.74407996137151),
            longitude=float(70.34136165403032)
        )
        return instance

    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'uzoxyzdfkulxwerfmxpt'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(25.74407996137151)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(70.34136165403032)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
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

