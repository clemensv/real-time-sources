"""
Test case for Notices
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_mqtt_producer_data.microsoft.opendata.us.noaa.stationtypes.notices import Notices


class Test_Notices(unittest.TestCase):
    """
    Test case for Notices
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Notices.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Notices for testing
        """
        instance = Notices(
            self_='jvarihwkkriutiwewzni'
        )
        return instance

    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'jvarihwkkriutiwewzni'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Notices.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Notices.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

