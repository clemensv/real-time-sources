"""
Test case for FareMedia
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.faremedia import FareMedia


class Test_FareMedia(unittest.TestCase):
    """
    Test case for FareMedia
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareMedia.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareMedia for testing
        """
        instance = FareMedia(
            fareMediaId='uziltyaggpdubgsyzleb',
            fareMediaName='arxvkpxqwrgfpgotxtdq',
            fareMediaDesc='xwbmhbvwadcauryydoju',
            fareMediaUrl='fcgbsvuomevjrfwsdmwy'
        )
        return instance

    
    def test_fareMediaId_property(self):
        """
        Test fareMediaId property
        """
        test_value = 'uziltyaggpdubgsyzleb'
        self.instance.fareMediaId = test_value
        self.assertEqual(self.instance.fareMediaId, test_value)
    
    def test_fareMediaName_property(self):
        """
        Test fareMediaName property
        """
        test_value = 'arxvkpxqwrgfpgotxtdq'
        self.instance.fareMediaName = test_value
        self.assertEqual(self.instance.fareMediaName, test_value)
    
    def test_fareMediaDesc_property(self):
        """
        Test fareMediaDesc property
        """
        test_value = 'xwbmhbvwadcauryydoju'
        self.instance.fareMediaDesc = test_value
        self.assertEqual(self.instance.fareMediaDesc, test_value)
    
    def test_fareMediaUrl_property(self):
        """
        Test fareMediaUrl property
        """
        test_value = 'fcgbsvuomevjrfwsdmwy'
        self.instance.fareMediaUrl = test_value
        self.assertEqual(self.instance.fareMediaUrl, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FareMedia.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FareMedia.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

