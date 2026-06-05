"""
Test case for Water
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_amqp_producer_data.de.wsv.pegelonline.water import Water


class Test_Water(unittest.TestCase):
    """
    Test case for Water
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Water.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Water for testing
        """
        instance = Water(
            shortname='mijgerxpmzwsrmnwvfbr',
            longname='iiokxusqcdmhpnwsmafs'
        )
        return instance

    
    def test_shortname_property(self):
        """
        Test shortname property
        """
        test_value = 'mijgerxpmzwsrmnwvfbr'
        self.instance.shortname = test_value
        self.assertEqual(self.instance.shortname, test_value)
    
    def test_longname_property(self):
        """
        Test longname property
        """
        test_value = 'iiokxusqcdmhpnwsmafs'
        self.instance.longname = test_value
        self.assertEqual(self.instance.longname, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Water.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Water.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

