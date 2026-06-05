"""
Test case for AvalancheRegion
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from eaws_albina_producer_data.avalancheregion import AvalancheRegion
import datetime


class Test_AvalancheRegion(unittest.TestCase):
    """
    Test case for AvalancheRegion
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AvalancheRegion.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AvalancheRegion for testing
        """
        instance = AvalancheRegion(
            region_id='xvtvwgxeysjhafsicgoi',
            lang='hsusrijisixncyqozlmi',
            configured_at=datetime.datetime.now(datetime.timezone.utc),
            bulletin_base_url='rbojgsxbrmjnuzvdhwuh'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'xvtvwgxeysjhafsicgoi'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'hsusrijisixncyqozlmi'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_configured_at_property(self):
        """
        Test configured_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.configured_at = test_value
        self.assertEqual(self.instance.configured_at, test_value)
    
    def test_bulletin_base_url_property(self):
        """
        Test bulletin_base_url property
        """
        test_value = 'rbojgsxbrmjnuzvdhwuh'
        self.instance.bulletin_base_url = test_value
        self.assertEqual(self.instance.bulletin_base_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AvalancheRegion.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AvalancheRegion.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

