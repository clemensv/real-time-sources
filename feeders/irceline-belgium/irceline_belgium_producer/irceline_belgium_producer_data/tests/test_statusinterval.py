"""
Test case for StatusInterval
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irceline_belgium_producer_data.statusinterval import StatusInterval


class Test_StatusInterval(unittest.TestCase):
    """
    Test case for StatusInterval
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StatusInterval.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StatusInterval for testing
        """
        instance = StatusInterval(
            lower='obnskvcxbjiitnsnzekc',
            upper='wtnhzxsqjrwagkvgfyqi',
            name='efjjumypbaldlurzhyzh',
            color='vkqlwcdzugxmjmcdakdl'
        )
        return instance

    
    def test_lower_property(self):
        """
        Test lower property
        """
        test_value = 'obnskvcxbjiitnsnzekc'
        self.instance.lower = test_value
        self.assertEqual(self.instance.lower, test_value)
    
    def test_upper_property(self):
        """
        Test upper property
        """
        test_value = 'wtnhzxsqjrwagkvgfyqi'
        self.instance.upper = test_value
        self.assertEqual(self.instance.upper, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'efjjumypbaldlurzhyzh'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_color_property(self):
        """
        Test color property
        """
        test_value = 'vkqlwcdzugxmjmcdakdl'
        self.instance.color = test_value
        self.assertEqual(self.instance.color, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StatusInterval.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StatusInterval.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

